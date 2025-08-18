package wtf.minjae.minjae_server.domain;

import java.io.File;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Getter
public class Video {

    private static final String VIDEO_PATH_FORMAT = "static/videos/%s.mp4";

    private final File videoFile;

    public Video(String baseVideo) {
        log.info("basevideo에 맞는 원본 비디오 파일 찾아오기");
        this.videoFile = new File(String.format(VIDEO_PATH_FORMAT, baseVideo));
        validateVideo(videoFile);
    }

    private void validateVideo(File videoResource) {
        if (!videoResource.exists()) {
            throw new IllegalArgumentException("Video does not exist");
        }
    }
}
