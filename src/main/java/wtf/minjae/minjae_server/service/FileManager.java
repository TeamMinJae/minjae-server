package wtf.minjae.minjae_server.service;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.nio.charset.StandardCharsets;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class FileManager {

    private static final String TEMP = "temp";

    public File createTempFile(String name, String content, String fileExtension) throws IOException {
        log.info(" 커스텀한 임시 자막 파일 저장");
        File dir = new File(TEMP);
        File tempFile = File.createTempFile(name, fileExtension, dir);
        try (Writer writer = new OutputStreamWriter(new FileOutputStream(tempFile), StandardCharsets.UTF_8)) {
            writer.write(content);
        }
        return tempFile;
    }

    public void deleteAll(File... files) {
        log.info(" 임시 파일 삭제");
        for (File file : files) {
            file.delete();
        }
    }
}
