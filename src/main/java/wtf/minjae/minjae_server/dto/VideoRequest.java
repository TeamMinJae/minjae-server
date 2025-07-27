package wtf.minjae.minjae_server.dto;

import java.util.List;

public record VideoRequest(
        String roomId,
        String winner,
        List<String> others,
        String baseVideo
) {
}
