const express = require('express');
const dotenv = require('dotenv');
const axios = require('axios');

dotenv.config();
const router = express.Router();

//ChatGPT code
const apiKey = process.env.OPENAI_API_KEY;

router.post('/chat', async(req, res) => {
    try{
        const {language, difficulty, topic, info} = req.body;
        const sentence = `Only give ${language} coding project outline that is ${difficulty} difficulty using ${topic} and ${info}`;

        const response = await axios.post(
            'https://api.openai.com/v1/completions', 
            {
                model: "gpt-3.5-turbo-instruct",
                prompt: sentence,
                max_tokens: 2048,
                temperature: 1,
            },
            {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${apiKey}`
                }
            } 
        );

        const answer = response.data.choices[0].text;
        //console.log(answer);
        res.status(200).json({ response: answer });
    }catch(err){
        console.error('Error:', err.response.data.error.message);
        res.status(500).send(err.response.data.error.message);
    }
});

module.exports = router;
