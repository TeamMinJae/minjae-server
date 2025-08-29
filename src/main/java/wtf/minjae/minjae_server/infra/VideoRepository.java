package wtf.minjae.minjae_server.infra;

import java.io.File;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import wtf.minjae.minjae_server.domain.Video;

@Component
@RequiredArgsConstructor
public class VideoRepository {

    @Value("${app.paths.video.dir}")
    private String videoDirectory;

    @Value("${app.paths.video.ext}")
    private String videoExtension;

    private final FileManager fileManager;

    public Video findBaseVideoByName(String name) {
        File baseVideoFile = fileManager.getStaticFile(videoDirectory, name, videoExtension);
        return new Video(baseVideoFile.getAbsolutePath());
    }
}
