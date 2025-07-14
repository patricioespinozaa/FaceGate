document.addEventListener('DOMContentLoaded', function () {
    const remoteVideo = document.getElementById('video-stream-student');
    const socket = io();
    const peer = new RTCPeerConnection();
    const pendingCandidates = [];

    peer.ontrack = (event) => {
        remoteVideo.srcObject = event.streams[0];
    };

    socket.on('offer', async ({ sdp }) => {
        await peer.setRemoteDescription(new RTCSessionDescription(sdp));
        const answer = await peer.createAnswer();
        await peer.setLocalDescription(answer);
        socket.emit('answer', { sdp: peer.localDescription });

        // Procesar ICE candidates que llegaron antes
        for (const candidate of pendingCandidates) {
            await peer.addIceCandidate(new RTCIceCandidate(candidate));
        }
        pendingCandidates.length = 0; // Limpia el buffer
    });

    peer.onicecandidate = (event) => {
        if (event.candidate) {
            socket.emit('ice-candidate', { candidate: event.candidate });
        }
    };

    socket.on('ice-candidate', ({ candidate }) => {
        if (peer.remoteDescription && peer.remoteDescription.type) {
            peer.addIceCandidate(new RTCIceCandidate(candidate));
        } else {
            pendingCandidates.push(candidate);
        }
    });
});
