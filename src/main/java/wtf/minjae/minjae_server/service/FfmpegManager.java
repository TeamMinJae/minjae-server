package wtf.minjae.minjae_server.service;

import java.io.File;
import java.io.IOException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class FfmpegManager {

    public File mergeVideoWithCaption(String roomId, File videoFile, File captionFile)
            throws IOException, InterruptedException {
        log.info(" ffmeg로 동영상+자막 명령어 만들기");
        log.info(" ffmeg 명렁어 실행");
        // 출력 파일 경로
        File outputFile = new File("temp/" + roomId + "_output.mp4");
        // FFmpeg 명령어 문자열 생성
        String[] command = generateCommand(videoFile, captionFile, outputFile);
        // 명령어 실행
        executeCommand(command);

        return outputFile;
    }

    private String[] generateCommand(File videoFile, File captionFile, File outputFile) {
        String[] command = {
                "ffmpeg",
                "-y", // 기존 파일 덮어쓰기
                "-i", videoFile.getAbsolutePath(), // 입력 비디오
                "-preset", "superfast",
                "-vf", "ass=" + captionFile.getAbsolutePath(), // 자막 필터
                "-c:a", "copy", // 오디오 복사
                outputFile.getAbsolutePath() // 출력 파일
        };
        return command;
    }

    private void executeCommand(String[] command) throws IOException, InterruptedException {
        ProcessBuilder pb = new ProcessBuilder(command);
        pb.redirectErrorStream(true); // stderr → stdout 통합
        Process process = pb.start();

        int exitCode = process.waitFor();
        if (exitCode != 0) {
            throw new RuntimeException("FFmpeg failed with exit code: " + exitCode);
        }
    }
}

