package wtf.minjae.minjae_server.service.caption;

import java.io.File;
import java.io.IOException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import wtf.minjae.minjae_server.domain.Caption;
import wtf.minjae.minjae_server.dto.VideoRequest;
import wtf.minjae.minjae_server.infra.CaptionRepository;

@Service
@RequiredArgsConstructor
public class CaptionService {

    private final CaptionCustomizer captionCustomizer;
    private final CaptionRepository captionRepository;

    public Caption customizeCaption(VideoRequest request, Caption caption) throws IOException {
        String customizedContent = captionCustomizer.customizeCaption(request, caption);
        return new Caption(customizedContent);
    }

    public File createTempCaption(String name, String customizedContent) throws IOException {
        return captionRepository.save(name, customizedContent);
    }

    public Caption getBaseCaption(String baseVideoName) throws IOException {
        return captionRepository.findBaseCaptionByName(baseVideoName);
    }
}
