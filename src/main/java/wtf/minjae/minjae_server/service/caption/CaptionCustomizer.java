package wtf.minjae.minjae_server.service.caption;

import java.io.IOException;
import wtf.minjae.minjae_server.domain.Caption;
import wtf.minjae.minjae_server.dto.VideoRequest;

public interface CaptionCustomizer {

    String customizeCaption(VideoRequest request, Caption caption) throws IOException;
}
