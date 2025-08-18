package wtf.minjae.minjae_server.service.caption;

import java.io.File;
import java.io.IOException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import wtf.minjae.minjae_server.domain.Caption;
import wtf.minjae.minjae_server.dto.VideoRequest;
import wtf.minjae.minjae_server.service.FileManager;

@Service
@RequiredArgsConstructor
public class CaptionService {

    private static final String CAPTION_EXTENSION = ".ass";

    private final CaptionCustomizer captionCustomizer;
    private final FileManager fileManager;

    public String customizeCaption(VideoRequest request, Caption caption) throws IOException {
        return captionCustomizer.customizeCaption(request, caption);
    }

    public Caption createTempCaption(String name, String customizedContent) throws IOException {
        File tempCaptionFile = fileManager.createTempFile(name, customizedContent, CAPTION_EXTENSION);
        return new Caption(tempCaptionFile);
    }
}
