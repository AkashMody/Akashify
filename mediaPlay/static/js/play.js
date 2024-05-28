function playNOW(track){
    var audio = document.getElementById('audio');
    //audio.pause();
    var playImg = document.getElementById('playnowIMG');
    var playTitle = document.getElementById('playnowTITLE');
    var playArtist = document.getElementById('playnowARTIST');
    var playTrack = document.getElementById('playnowTRACK');
    var fetchURL = "/playnow/" + track
    playTrack.src = //url of song
    fetch(fetchURL)
    .then(response => {
            if(response.ok){
                console.log('Track Promise resolved and HTTP status is successful');
                return response.json()
            }else{
                if (response.status === 404) throw new Error('404, Not found');
                if (response.status === 500) throw new Error('500, internal server error');
                throw new Error(response.status);
            }
    })
    .then(data => {
        //console.log(data)
        playImg.src = data.img
        playTitle.innerHTML = data.title
        playArtist.innerHTML = data.artist
        playTrack.src = data.track
        audio.load()
    }).catch(error => {
            console.error("Fetch:",error);
    })
    
    //audio.play(); 
}
