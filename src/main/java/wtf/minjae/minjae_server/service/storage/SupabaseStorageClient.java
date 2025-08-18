package wtf.minjae.minjae_server.service.storage;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
@Slf4j
public class SupabaseStorageClient implements StorageClient {

    public static final String STORAGE_PATH = "/storage/v1/object/";

    @Value("${supabase.url}")
    private String supabaseUrl;

    @Value("${supabase.api-key}")
    private String supabaseKey;

    @Value("${supabase.bucket}")
    private String bucket;

    @Override
    public String upload(String roomId, File outputVideoFile) throws IOException {
        log.info("storage에 저장");

        String objectPath = bucket + "/" + roomId + "_output.mp4";
        String uploadUrl = supabaseUrl + STORAGE_PATH + objectPath;
        byte[] videoBytes = Files.readAllBytes(outputVideoFile.toPath());

        HttpHeaders headers = new HttpHeaders();
        headers.setBearerAuth(supabaseKey);
        headers.setContentType(MediaType.valueOf("video/mp4"));
        headers.setContentLength(videoBytes.length);
        headers.add("x-upsert", "true");

        HttpEntity<byte[]> entity = new HttpEntity<>(videoBytes, headers);
        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<String> response = restTemplate.exchange(uploadUrl, HttpMethod.POST, entity, String.class);

        System.out.println("response = " + response);

        return supabaseUrl + STORAGE_PATH + "public/" + objectPath;
    }
}
