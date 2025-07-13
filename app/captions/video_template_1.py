# app/captions/video_template_1.py
from typing import List, Dict, Any


def generate_captions_for_video1(winner: str, others: List[str]) -> List[Dict[str, Any]]:

    template_captions = [
        {"text": f"{winner} : 하 ㅅㅂ", "x": 1920/2 + (0.0 / 2), "y": 1080 / 2 - (822.633 / 2), "start": 122122/24000, "duration": 36036 / 24000},
        {"text": f"{others[0 % len(others)]} : 누가 걸렸음?", "x": 1920/2 + (4.98517e-10 / 2), "y": 1080 / 2 - (822.633 / 2), "start": 158158/24000, "duration": 29029 / 24000},
        {"text": f"{others[1 % len(others)]} : {winner}임 ㅋㅋㅋㅋ8", "x": 1920/2 + (4.06838e-10 / 2), "y": 1080 / 2 - (706.982 / 2), "start": 187187/24000, "duration": 33033 / 24000},
        {"text": f"{others[2 % len(others)]} : (웃참중)", "x": 1920/2 -(21.6055 / 2), "y": 1080 / 2 - (757.321 / 2), "start": 220220/24000, "duration": 29029 / 24000},
        {"text": f"{others[3 % len(others)]} : ㅋㅋ {winner} ㅅㄱ", "x": 1920/2 + (598.073 / 2), "y": 1080 / 2 - (744.165 / 2), "start": 249249/24000, "duration": 29029 / 24000},
        {"text": f"{others[4 % len(others)]} : ㅋㅋ ㅅㄱㅅㄱ", "x": 1920/2 -(599.284 / 2), "y": 1080 / 2 - (646.789 / 2), "start": 278278/24000, "duration": 29029 / 24000},
        {"text": f"{others[5 % len(others)]} : 아이고 어떡하냐", "x": 1920/2 + (541.211 / 2), "y": 1080 / 2 - (660.661 / 2), "start": 307307/24000, "duration": 29029 / 24000},
        {"text": f"{others[6 % len(others)]} : (눈치없이 개좋아 하는중)", "x": 1920/2 -(592.541 / 2), "y": 1080 / 2 - (733.321 / 2), "start": 336336/24000, "duration": 28028 / 24000},
        {"text": f"{others[7 % len(others)]} : {winner}, 땡큐~", "x": 1920/2 + (494.505 / 2), "y": 1080 / 2 - (778.541 / 2), "start": 364364/24000, "duration": 33033 / 24000},
        {"text": f"{others[8 % len(others)]} : 꽤겍 께게겍", "x": 1920/2 -(34.3486 / 2), "y": 1080 / 2 - (741.495 / 2), "start": 397397/24000, "duration": 30030 / 24000},
        {"text": f"{others[9 % len(others)]} : ㅎㅎ 나 아니네", "x": 1920/2 -(743.45 / 2), "y": 1080 / 2 - (756.303 / 2), "start": 427427/24000, "duration": 29029 / 24000},
        {"text": f"{others[10 % len(others)]} : 다행이다 ㅋㅋ", "x": 1920/2 + (718.982 / 2), "y": 1080 / 2 - (759.936 / 2), "start": 456456/24000, "duration": 32032 / 24000},
        {"text": f"{others[11 % len(others)]} : 개꿀 ㅋㅋ", "x": 1920/2 -(652.982 / 2), "y": 1080 / 2 - (812.752 / 2), "start": 488488/24000, "duration": 29029 / 24000},
        {"text": f"{others[12 % len(others)]} : ㅋ", "x": 1920/2 + (705.716 / 2), "y": 1080 / 2 - (684.055 / 2), "start": 517517/24000, "duration": 33033 / 24000},
        {"text": "아빠", "x": 1920/2 - (389.6 / 2), "y": 1080 / 2 - (729.139 / 2), "start": 550550/24000, "duration": 42042 / 24000},
        {"text": "엄마", "x": 1920/2 + (495.936 / 2), "y": 1080 / 2 - (512.642 / 2), "start": 550550/24000, "duration": 42042 / 24000},
        {"text": f"{winner} : ㅜㅜ", "x": 1920/2 + (8.66862e-12 / 2), "y": 1080 / 2 - (782.174 / 2), "start": 592592/24000, "duration": 65065 / 24000},
    ]

    return template_captions


"""
                        <asset-clip ref="r2" offset="122122/24000s" name="SSYouTube.online_Omedetou - Evangelion_1080p" start="310310/24000s" duration="36036/24000s" format="r3" tcFormat="NDF" audioRole="dialogue">
                            <title ref="r6" lane="1" offset="310310/24000s" name="걸린사람 - 텍스트" start="86486400/24000s" duration="36036/24000s" enabled="0">
                                <param name="Build In" key="9999/10000/2/101" value="0"/>
                                <param name="Build Out" key="9999/10000/2/102" value="0"/>
                                <param name="위치" key="9999/10003/13260/3296672360/1/100/101" value="0 822.633"/>



<asset-clip ref="r2" offset="158158/24000s" name="SSYouTube.online_Omedetou - Evangelion_1080p" start="346346/24000s" duration="29029/24000s" format="r3" tcFormat="NDF" audioRole="dialogue">
                            <title ref="r6" lane="1" offset="346346/24000s" name="사람 1 - 텍스트" start="86486400/24000s" duration="29029/24000s" enabled="0">
                                <param name="위치" key="9999/10003/13260/3296672360/1/100/101" value="4.98517e-10 822.633"/>
<asset-clip ref="r2" offset="187187/24000s" name="SSYouTube.online_Omedetou - Evangelion_1080p" start="375375/24000s" duration="33033/24000s" format="r3" tcFormat="NDF" audioRole="dialogue">
                            <title ref="r6" lane="1" offset="375375/24000s" name="사람 2 - 텍스트" start="86486400/24000s" duration="33033/24000s" enabled="0">
                                <param name="위치" key="9999/10003/13260/3296672360/1/100/101" value="4.06838e-10 706.982"/>
<asset-clip ref="r2" offset="220220/24000s" name="SSYouTube.online_Omedetou - Evangelion_1080p" start="408408/24000s" duration="29029/24000s" format="r3" tcFormat="NDF" audioRole="dialogue">
                            <title ref="r6" lane="1" offset="408408/24000s" name="사람 3 - 텍스트" start="86486400/24000s" duration="29029/24000s" enabled="0">
                                <param name="위치" key="9999/10003/13260/3296672360/1/100/101" value="-21.6055 757.321"/>
<asset-clip ref="r2" offset="249249/24000s" name="SSYouTube.online_Omedetou - Evangelion_1080p" start="437437/24000s" duration="29029/24000s" format="r3" tcFormat="NDF" audioRole="dialogue">
                            <title ref="r6" lane="1" offset="437437/24000s" name="사람 4 - 텍스트" start="86486400/24000s" duration="29029/24000s" enabled="0">
                                <param name="위치" key="9999/10003/13260/3296672360/1/100/101" value="598.073 744.165"/>
<asset-clip ref="r2" offset="278278/24000s" name="SSYouTube.online_Omedetou - Evangelion_1080p" start="466466/24000s" duration="29029/24000s" format="r3" tcFormat="NDF" audioRole="dialogue">
                            <title ref="r6" lane="1" offset="466466/24000s" name="사람 5 - 텍스트" start="86486400/24000s" duration="29029/24000s" enabled="0">
                                <param name="위치" key="9999/10003/13260/3296672360/1/100/101" value="-599.284 646.789"/>
<asset-clip ref="r2" offset="307307/24000s" name="SSYouTube.online_Omedetou - Evangelion_1080p" start="495495/24000s" duration="29029/24000s" format="r3" tcFormat="NDF" audioRole="dialogue">
                            <title ref="r6" lane="1" offset="495495/24000s" name="사람 6 - 텍스트" start="86486400/24000s" duration="29029/24000s" enabled="0">
                                <param name="위치" key="9999/10003/13260/3296672360/1/100/101" value="541.211 660.661"/>
<asset-clip ref="r2" offset="336336/24000s" name="SSYouTube.online_Omedetou - Evangelion_1080p" start="524524/24000s" duration="28028/24000s" format="r3" tcFormat="NDF" audioRole="dialogue">
                            <title ref="r6" lane="1" offset="524524/24000s" name="사람 7 - 텍스트" start="86486400/24000s" duration="28028/24000s" enabled="0">
                                <param name="위치" key="9999/10003/13260/3296672360/1/100/101" value="-592.541 733.321"/>
<asset-clip ref="r2" offset="364364/24000s" name="SSYouTube.online_Omedetou - Evangelion_1080p" start="552552/24000s" duration="33033/24000s" format="r3" tcFormat="NDF" audioRole="dialogue">
                            <title ref="r6" lane="1" offset="552552/24000s" name="사람 8 - 텍스트" start="86486400/24000s" duration="33033/24000s" enabled="0">
                                <param name="위치" key="9999/10003/13260/3296672360/1/100/101" value="494.505 778.541"/>
<asset-clip ref="r2" offset="397397/24000s" name="SSYouTube.online_Omedetou - Evangelion_1080p" start="585585/24000s" duration="30030/24000s" format="r3" tcFormat="NDF" audioRole="dialogue">
                            <title ref="r6" lane="1" offset="585585/24000s" name="사람 9 - 텍스트" start="86486400/24000s" duration="30030/24000s" enabled="0">
                                <param name="위치" key="9999/10003/13260/3296672360/1/100/101" value="-34.3486 741.495"/>
<asset-clip ref="r2" offset="427427/24000s" name="SSYouTube.online_Omedetou - Evangelion_1080p" start="615615/24000s" duration="29029/24000s" format="r3" tcFormat="NDF" audioRole="dialogue">
                            <title ref="r6" lane="1" offset="615615/24000s" name="사람 10 - 텍스트" start="86486400/24000s" duration="29029/24000s" enabled="0">
                                <param name="위치" key="9999/10003/13260/3296672360/1/100/101" value="-743.45 756.303"/>
<asset-clip ref="r2" offset="456456/24000s" name="SSYouTube.online_Omedetou - Evangelion_1080p" start="644644/24000s" duration="32032/24000s" format="r3" tcFormat="NDF" audioRole="dialogue">
                            <title ref="r6" lane="1" offset="644644/24000s" name="사람 11 - 텍스트" start="86486400/24000s" duration="32032/24000s" enabled="0">
                                <param name="위치" key="9999/10003/13260/3296672360/1/100/101" value="718.982 759.936"/>
<asset-clip ref="r2" offset="488488/24000s" name="SSYouTube.online_Omedetou - Evangelion_1080p" start="676676/24000s" duration="29029/24000s" format="r3" tcFormat="NDF" audioRole="dialogue">
                            <title ref="r6" lane="1" offset="676676/24000s" name="사람 12 - 텍스트" start="86486400/24000s" duration="29029/24000s" enabled="0">
                                <param name="위치" key="9999/10003/13260/3296672360/1/100/101" value="-652.982 812.752"/>
<asset-clip ref="r2" offset="517517/24000s" name="SSYouTube.online_Omedetou - Evangelion_1080p" start="705705/24000s" duration="33033/24000s" format="r3" tcFormat="NDF" audioRole="dialogue">
                            <title ref="r6" lane="1" offset="705705/24000s" name="사람 13 - 텍스트" start="86486400/24000s" duration="33033/24000s" enabled="0">
                                <param name="위치" key="9999/10003/13260/3296672360/1/100/101" value="705.716 684.055"/>
<asset-clip ref="r2" offset="550550/24000s" name="SSYouTube.online_Omedetou - Evangelion_1080p" start="738738/24000s" duration="42042/24000s" format="r3" tcFormat="NDF" audioRole="dialogue">
                            <title ref="r6" lane="1" offset="738738/24000s" name="아빠 - 텍스트" start="86486400/24000s" duration="42042/24000s" enabled="0">
                                <param name="위치" key="9999/10003/13260/3296672360/1/100/101" value="-389.6 729.139"/>
                            <title ref="r6" lane="2" offset="738738/24000s" name="엄마 - 텍스트" start="86486400/24000s" duration="42042/24000s" enabled="0">
                                <param name="위치" key="9999/10003/13260/3296672360/1/100/101" value="495.936 512.642"/>
<asset-clip ref="r2" offset="592592/24000s" name="SSYouTube.online_Omedetou - Evangelion_1080p" start="780780/24000s" duration="65065/24000s" format="r3" tcFormat="NDF" audioRole="dialogue">
                            <title ref="r6" lane="1" offset="780780/24000s" name="걸린사람 - 텍스트" start="86486400/24000s" duration="65065/24000s" enabled="0">
                                <param name="위치" key="9999/10003/13260/3296672360/1/100/101" value="8.66862e-12 782.174"/>

"""
