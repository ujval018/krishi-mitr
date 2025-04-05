# Krishi Mitr - Farmer's Friend Platform

![Krishi Mitr Logo](https://example.com/logo.png) *[Note: Add actual logo path later]*

Krishi Mitr is a farmer-to-farmer platform that enables:
- Crop bartering between farmers
- Direct crop sales
- Community building for agricultural knowledge sharing

## Features

### User Authentication
- Secure registration and login
- User profile management

### Crop Management
- Add crops for barter or sale
- Browse available crops
- Complete barter/purchase transactions

### Database
- Simple JSON-based storage
- Easy to backup and migrate

## Technology Stack

### Backend
- Python Flask (API server)
- JSON database

### Frontend
- HTML/CSS/JavaScript
- Responsive design

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js (for frontend)
- Git

### Installation
1. Clone the repository:
```bash
git clone https://github.com/your-repo/krishi-mitr.git
cd krishi-mitr
```

2. Set up backend:
```bash
cd backend
pip install -r requirements.txt
```

3. Set up frontend:
```bash
cd ../frontend
npm install
```

### Running the Application
1. Start backend server:
```bash
cd backend
python app.py
```

2. Start frontend development server:
```bash
cd ../frontend
npm start
```

3. Access the application at `http://localhost:3000`

## API Documentation

The backend API follows REST conventions and includes:

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Authenticate user

### Crop Operations
- `POST /api/crop/add` - Add new crop
- `GET /api/crop/list` - List available crops
- `POST /api/crop/barter/<crop_id>` - Barter a crop
- `POST /api/crop/buy/<crop_id>` - Purchase a crop

For detailed API documentation including request/response examples, see [API_DOCS.md](API_DOCS.md).

## Project Structure

```
krishi-mitr/
├── backend/            # Flask API server
│   ├── app.py          # Main application
│   ├── routes/         # Route definitions
│   └── database.json   # JSON database
├── frontend/           # Web interface
│   ├── public/         # Static assets
│   ├── scripts/        # JavaScript files
│   └── styles/         # CSS files
├── README.md           # This file
└── API_DOCS.md         # API documentation
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Project Maintainer: [Your Name] - your.email@example.com

Project Link: [https://github.com/your-repo/krishi-mitr](https://github.com/your-repo/krishi-mitr)
