package wtf.minjae.minjae_server.domain;

import lombok.Getter;

@Getter
public class Caption {

    private final String content;

    public Caption(String content) {
        this.content = content;
    }
}
