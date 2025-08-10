package wtf.minjae.minjae_server.service;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import wtf.minjae.minjae_server.dto.VideoRequest;
import wtf.minjae.minjae_server.dto.VideoResponse;

@Service
@Slf4j
public class VideoService {

    private static final String VIDEO_PATH_FORMAT = "static/videos/%s.mp4";
    private static final String SUBSCRIPTION_PATH_FORMAT = "static/subscriptions/%s.ass";
    private static final String DELIMETER = "##";

    @Value("${supabase.url}")
    private String supabaseUrl;

    @Value("${supabase.api-key}")
    private String supabaseKey;

    @Value("${supabase.bucket}")
    private String buket;

    public VideoResponse generateVideo(VideoRequest request) throws IOException, InterruptedException {
        //basevideo에 맞는 원본 자막 파일 찾아오기
        log.info("basevideo에 맞는 원본 자막 파일 찾아오기");
        File videoFile = new File(String.format(VIDEO_PATH_FORMAT, request.baseVideo()));
        validateVideo(videoFile);

        File subscriptionFile = new File(String.format(SUBSCRIPTION_PATH_FORMAT, request.baseVideo()));
        validateSubscription(subscriptionFile);

        // 자막 파일 열어서 커스텀하기
        log.info(" 자막 파일 열어서 커스텀하기");
        String content = Files.readString(subscriptionFile.toPath(), StandardCharsets.UTF_8);
        String customizedContent = customizeSubscription(request, content);

        // 커스텀한 임시 자막 파일 저장
        log.info(" 커스텀한 임시 자막 파일 저장");
        File dir = new File("temp");
        File customSubscription = File.createTempFile(request.roomId(), ".ass", dir);
        try (Writer writer = new OutputStreamWriter(new FileOutputStream(customSubscription), StandardCharsets.UTF_8)) {
            writer.write(customizedContent);
        }

        // ffmeg로 동영상+자막 명령어 만들기
        log.info(" ffmeg로 동영상+자막 명령어 만들기");
        // ffmeg 명렁어 실행
        log.info(" ffmeg 명렁어 실행");
        File outputVideo = mergeVideoWithSubtitle(request.roomId(), videoFile,
                customSubscription);

        // storage에 저장
        log.info(" storage에 저장");
        String objectPath = upload(request, outputVideo);

        // 임시 자막 파일 삭제
        log.info(" 임시 자막 파일 삭제");
        customSubscription.delete();
        outputVideo.delete();

        //url return
        log.info("url return");
        return new VideoResponse(supabaseUrl +"/storage/v1/object/public/"+ objectPath);
    }

    private String customizeSubscription(VideoRequest request, String content) {
        //이름 바꾸기
        if (content.contains(DELIMETER + "winner" + DELIMETER)) {
            content = content.replaceAll(DELIMETER + "winner" + DELIMETER, request.winner());
        }
        for (int i = 0; i < 20; i++) {
            List<String> others = request.others();
            if (content.contains(DELIMETER + "other" + i + "##")) {
                content = content.replaceAll(DELIMETER + "other" + i + DELIMETER, others.get(i % others.size()));
            }
        }
        return content;
    }

    private void validateVideo(File videoResource) {
        if (!videoResource.exists()) {
            throw new IllegalArgumentException("Video does not exist");
        }
    }

    private void validateSubscription(File subscriptionResource) {
        if (!subscriptionResource.exists()) {
            throw new IllegalArgumentException("Subscription does not exist");
        }
    }

    private File mergeVideoWithSubtitle(String roomId, File videoFile, File subtitleFile)
            throws IOException, InterruptedException {
        // 출력 파일 경로
        File outputFile = new File("temp/" + roomId + "_output.mp4");

        // FFmpeg 명령어 문자열 생성
        String[] command = {
                "ffmpeg",
                "-y", // 기존 파일 덮어쓰기
                "-i", videoFile.getAbsolutePath(), // 입력 비디오
                "-preset", "superfast",
                "-vf", "ass=" + subtitleFile.getAbsolutePath(), // 자막 필터
                "-c:a", "copy", // 오디오 복사
                outputFile.getAbsolutePath() // 출력 파일
        };

        // 명령어 실행
        ProcessBuilder pb = new ProcessBuilder(command);
        pb.redirectErrorStream(true); // stderr → stdout 통합
        Process process = pb.start();

        int exitCode = process.waitFor();
        if (exitCode != 0) {
            throw new RuntimeException("FFmpeg failed with exit code: " + exitCode);
        }

        return outputFile;
    }

    private String upload(VideoRequest request, File outputFile) throws IOException {

        String objectPath = buket + "/" + request.roomId() + "_output.mp4";
        String uploadUrl = supabaseUrl + "/storage/v1/object/" + objectPath;
        byte[] videoBytes = Files.readAllBytes(outputFile.toPath());

        HttpHeaders headers = new HttpHeaders();
        headers.setBearerAuth(supabaseKey);
        headers.setContentType(MediaType.valueOf("video/mp4"));
        headers.setContentLength(videoBytes.length);
        headers.add("x-upsert", "true");

        HttpEntity<byte[]> entity = new HttpEntity<>(videoBytes, headers);
        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<String> response = restTemplate.exchange(uploadUrl, HttpMethod.POST, entity, String.class);

        System.out.println("response = " + response);

        return objectPath;
    }
}

