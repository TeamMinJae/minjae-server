package wtf.minjae.minjae_server.controller;

import java.io.IOException;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import wtf.minjae.minjae_server.dto.VideoRequest;
import wtf.minjae.minjae_server.dto.VideoResponse;
import wtf.minjae.minjae_server.service.VideoService;

@RestController
@RequiredArgsConstructor
public class VideoController {

    private final VideoService videoService;

    @PostMapping("/videos")
    public VideoResponse generateVideo(@RequestBody VideoRequest request) throws IOException, InterruptedException {
        return videoService.generateVideo(request);
    }
}
