package wtf.minjae.minjae_server.infra;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class FileManager {

    @Value("${app.paths.roots.static}")
    private String staticPath;

    @Value("${app.paths.roots.temp}")
    private String tempPath;

    public File createTempFile(String name, String content, String fileExtension) throws IOException {
        log.info(" 커스텀한 임시 자막 파일 저장");
        File dir = new File(tempPath);
        File tempFile = File.createTempFile(name, fileExtension, dir);
        try (Writer writer = new OutputStreamWriter(new FileOutputStream(tempFile), StandardCharsets.UTF_8)) {
            writer.write(content);
        }
        return tempFile;
    }

    public File getStaticFile(String directory, String name, String fileExtension) {
        log.info("원본 {} 파일 찾아오기", directory);
        Path path = Paths.get(staticPath, directory, name + fileExtension);
        File staticFile = path.toFile();
        validate(staticFile);
        return staticFile;
    }

    public String readFile(String path) throws IOException {
        File resourceFile = new File(path);
        validate(resourceFile);
        return Files.readString(resourceFile.toPath(), StandardCharsets.UTF_8);
    }

    private void validate(File fileResource) {
        if (!fileResource.exists()) {
            throw new IllegalArgumentException("File does not exist");
        }
    }

    public void deleteAll(File... files) {
        log.info(" 임시 파일 삭제");
        for (File file : files) {
            file.delete();
        }
    }
}
