package wtf.minjae.minjae_server.service.caption;

import java.io.IOException;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import wtf.minjae.minjae_server.domain.Caption;
import wtf.minjae.minjae_server.dto.VideoRequest;

@Component
@Slf4j
public class OmedettoCustomizer implements CaptionCustomizer {

    private static final String DELIMITER = "##";

    @Override
    public String customizeCaption(VideoRequest request, Caption caption) throws IOException {
        log.info(" 자막 파일 열어서 커스텀하기");
        String content = caption.getContent();
        if (content.contains(DELIMITER + "winner" + DELIMITER)) {
            content = content.replaceAll(DELIMITER + "winner" + DELIMITER, request.winner());
        }
        for (int i = 0; i < 20; i++) {
            List<String> others = request.others();
            if (content.contains(DELIMITER + "other" + i + "##")) {
                content = content.replaceAll(DELIMITER + "other" + i + DELIMITER, others.get(i % others.size()));
            }
        }
        return content;
    }
}
