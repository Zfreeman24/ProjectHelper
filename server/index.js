const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const dotenv = require("dotenv");
const bodyParser = require("body-parser");
const bcrypt = require("bcrypt");
const usersModel = require("./models/users");
const chatRoute = require("./routes/chatRoutes");
const session = require('express-session');
const crypto = require('crypto');

const app = express();

// Middleware setup
app.use(express.json());
app.use(cors());
app.use(bodyParser.json());

// Load environment variables
dotenv.config();

// MongoDB connection
const MONGODB_URI = process.env.MONGODB_URI;
mongoose.connect(MONGODB_URI, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log("Connected to MongoDB"))
    .catch(err => console.error("MongoDB connection error:", err));

const generateRandomSecret = () => {
    return crypto.randomBytes(32).toString('hex'); 
};

//Create user session 
app.use(session({
    secret: generateRandomSecret(), 
    resave: false,
    saveUninitialized: false,
    cookie: { maxAge: 3600000 } //session expiration is 1 hour
}));

//check if user session is valid
app.get('/check-auth', (req, res) => {
    if (req.session && req.session.user) {
      res.sendStatus(200); //Authorized
    } else {
      res.sendStatus(401); //Unauthorized
    }
  });


// Chat route
app.use("/", chatRoute);

// User registration route
app.post("/register", async (req, res) => {
    try {
        const { email, password } = req.body;

        console.log("Registration request received:", req.body);

        const existingUser = await usersModel.findOne({ email });

        if (existingUser) {
            return res.json({ message: "Existing account" });
        }

        const hashedPassword = await bcrypt.hash(password, 10);
        const newUser = await usersModel.create({ email, password: hashedPassword });

        console.log("User registered successfully:", newUser);

        res.status(201).json({ user: newUser, message: "Created account" });
    } catch (err) {
        console.error("Error registering user:", err);
        res.status(500).json({ error: "Internal server error" });
    }
});

// User login route
app.post("/login", async (req, res) => {
    try {
        const { email, password } = req.body;
        const user = await usersModel.findOne({ email });

        if (!user) {
            return res.json("Wrong email");
        }

        const passwordMatch = await bcrypt.compare(password, user.password);
        if (passwordMatch) {
            req.session.user = user; //Set the user session
            res.json("Success");
        } else {
            res.json("Wrong password");
        }
    } catch (err) {
        console.error("Error logging in:", err);
        res.status(500).json({ error: "Internal server error" });
    }
});

//User logout route
app.get('/logout', (req, res) => {
    req.session.destroy(err => {
        if (err) {
            console.error("Error destroying session:", err);
            res.sendStatus(500).json({ error: "Internal server error" });
        } else {
            res.sendStatus(200);
        }
    });
});


// Start server
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
