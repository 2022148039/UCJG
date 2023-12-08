  
const express = require('express');
const multer  = require('multer');
const path = require('path');
const {spawn} = require('child_process');
const { traceDeprecation } = require('process');
const fs = require("fs");
const app = express();

app.use(express.static(path.join(__dirname, 'public')));
app.use('/picture', express.static(__dirname + '/picture'));
app.use('/picture_exhibition', express.static(__dirname + '/picture_exhibition'));

app.use('/picture_result', express.static(__dirname + '/picture_result'));

// Set up multer disk storage
const storagePage1 = multer.diskStorage({
    destination: function (req, file, cb) {
      cb(null, 'picture_exhibition/')
    },
    filename: function (req, file, cb) {
      cb(null, file.originalname)
    }
  })
  
const uploadPage1 = multer({ storage: storagePage1 })
  
  // Set up multer disk storage for page2
  const storagePage2 = multer.diskStorage({
    destination: function (req, file, cb) {
      cb(null, 'picture/')
    },
    filename: function (req, file, cb) {
      cb(null, file.originalname)
    }
  })
  
  const uploadPage2 = multer({ storage: storagePage2 })

  app.get('/get_picture_images', (req, res) => {
    const pictureDir = './picture';
    fs.readdir(pictureDir, (err, files) => {
        res.json(files);
    });
  });
  
  app.get('/get_picture_result_images', (req, res) => {
    const pictureResultDir = './picture_result';
    fs.readdir(pictureResultDir, (err, files) => {
        res.json(files);
    });
  });

  app.get('/get_picture_exhibition_image', (req, res) => {
    const pictureExhibitionResultDir = './picture_exhibition';
    fs.readdir(pictureExhibitionResultDir, (err, files) => {
        res.json(files);
    });
  });


app.listen(8080, () => {
    console.log('Server running at http://localhost:8080');
});


// 서버에서 이미지들을 `picture` 폴더로 업로드하는 코드
app.post('/upload_picture', uploadPage2.array('pictures[]', 12), function (req, res, next) {
  console.log(req.files);
  // 파이썬 스크립트 실행
  const python = spawn('python',['picture.py']);

  let outputData="";

  python.stdout.on('data',(data)=>{
    outputData += data.toString();
  });

  python.stdout.on('end',()=>{
    // 파이썬 스크립트 실행 후 결과를 받아옴
    console.log(outputData);
    res.redirect('/last.html');
  });

  python.on('error',(err)=>{
    console.error(err.message);
  });

  python.on('close',(code)=>{
    if(code!==0){
      console.error(`Python process exited with code ${code}`);
    }
    
  });
  python.stderr.on('data',(data)=>{
    console.error(`Python stderr:  ${data}`);
  });
});

app.post('/upload_picture_exhibition', uploadPage1.array('pictures[]', 1), function (req, res, next) {
  console.log(req.files);
  // Execute the first Python script
  const python = spawn('python', ['atmo_music.py']);
  
  let outputData = "";

  python.stdout.on('data', (data) => {
    outputData += data.toString();
  });

  python.on('error', (err) => {
    console.error(err.message);
  });

  python.stderr.on('data', (data) => {
    console.error(`Python stderr from first Python script: ${data}`);
  });

  python.on('close', (code) => {
    if (code !== 0) {
      console.error(`Python process exited with code ${code}`);
    } else {
      // If the first Python script executed successfully, execute the second one
      const python1 = spawn('python', ['music_generation.py']);

      python1.stdout.on('data', (data) => {
        console.log(`Output from second Python script: ${data}`);
      });

      python1.stderr.on('data', (data) => {
        console.error(`Python stderr from second Python script: ${data}`);
      });

      python1.on('close', (code) => {
        if (code !== 0) {
          console.error(`Second Python process exited with code ${code}`);
        } else {
          // If the second Python script also executed successfully, then redirect
          res.redirect('/page2.html');
        }
      });
    }
  });
});
app.get('/download_music', function(req, res) {
  const file = `${__dirname}/output.mid`;  // 파일 경로 설정
  res.download(file); // 다운로드 시작
});
app.get('/download_rgb', function(req, res) {
  const file = `${__dirname}/rgb.txt`;  // 파일 경로 설정
  res.download(file); // 다운로드 시작
});
app.use('/rgb_values', express.static(__dirname + '/'));

