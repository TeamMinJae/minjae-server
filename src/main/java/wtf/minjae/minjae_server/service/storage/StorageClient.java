package wtf.minjae.minjae_server.service.storage;

import java.io.File;
import java.io.IOException;

public interface StorageClient {
    String upload(String name, File file) throws IOException;
}
