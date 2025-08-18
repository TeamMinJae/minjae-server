package wtf.minjae.minjae_server.domain;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Getter
public class Caption {

    private static final String CAPTION_PATH_FORMAT = "static/captions/%s.ass";

    private final File captionFile;

    public Caption(String baseVideo) {
        log.info("basevideo에 맞는 원본 자막 파일 찾아오기");
        this.captionFile = new File(String.format(CAPTION_PATH_FORMAT, baseVideo));
        validateCaption(captionFile);
    }

    public Caption(File captionFile) {
        this.captionFile = captionFile;
        validateCaption(captionFile);
    }

    private void validateCaption(File captionResource) {
        if (!captionResource.exists()) {
            throw new IllegalArgumentException("Caption does not exist");
        }
    }

    public String getContent() throws IOException {
        return Files.readString(captionFile.toPath(), StandardCharsets.UTF_8);
    }
}
