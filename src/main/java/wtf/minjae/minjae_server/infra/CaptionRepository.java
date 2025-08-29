package wtf.minjae.minjae_server.infra;

import java.io.File;
import java.io.IOException;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import wtf.minjae.minjae_server.domain.Caption;

@Component
@RequiredArgsConstructor
public class CaptionRepository {

    @Value("${app.paths.caption.dir}")
    private String captionDirectory;

    @Value("${app.paths.caption.ext}")
    private String captionExtension;

    private final FileManager fileManager;

    public Caption findBaseCaptionByName(String name) throws IOException {
        File baseCaptionFile = fileManager.getStaticFile(captionDirectory, name, captionExtension);
        String content = fileManager.readFile(baseCaptionFile.getAbsolutePath());
        return new Caption(content);
    }

    public File save(String name, String customizedContent) throws IOException {
        return fileManager.createTempFile(name, customizedContent, captionExtension);
    }
}
