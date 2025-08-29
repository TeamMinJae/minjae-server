package wtf.minjae.minjae_server.domain;

import lombok.Getter;

@Getter
public class Video {

    private final String path;

    public Video(String path) {
        this.path = path;
    }
}
