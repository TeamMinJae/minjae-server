package wtf.minjae.minjae_server.service;

import java.io.File;
import java.io.IOException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import wtf.minjae.minjae_server.domain.Caption;
import wtf.minjae.minjae_server.domain.Video;
import wtf.minjae.minjae_server.dto.VideoRequest;
import wtf.minjae.minjae_server.dto.VideoResponse;
import wtf.minjae.minjae_server.infra.FfmpegManager;
import wtf.minjae.minjae_server.infra.FileManager;
import wtf.minjae.minjae_server.infra.VideoRepository;
import wtf.minjae.minjae_server.service.caption.CaptionService;
import wtf.minjae.minjae_server.service.storage.StorageClient;

@Service
@Slf4j
@RequiredArgsConstructor
public class VideoService {

    private final CaptionService captionService;
    private final VideoRepository videoRepository;
    private final FileManager fileManager;
    private final FfmpegManager ffmpegManager;
    private final StorageClient storageClient;

    public VideoResponse generateVideo(VideoRequest request) throws IOException, InterruptedException {
        Video baseVideo = videoRepository.findBaseVideoByName(request.baseVideo());
        Caption baseCaption = captionService.getBaseCaption(request.baseVideo());
        Caption customizedCaption = captionService.customizeCaption(request, baseCaption);
        File tempCaptionFile = captionService.createTempCaption(request.roomId(), customizedCaption.getContent());

        File outputVideoFile = ffmpegManager.mergeVideoWithCaption(
                request.roomId(),
                baseVideo.getPath(),
                tempCaptionFile.getAbsolutePath()
        );
        String videoUrl = storageClient.upload(request.roomId(), outputVideoFile);

        fileManager.deleteAll(
                tempCaptionFile,
                outputVideoFile
        );

        log.info("url return");
        return new VideoResponse(videoUrl);
    }
}

