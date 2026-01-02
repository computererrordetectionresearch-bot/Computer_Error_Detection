# Shop Recommendation Engine - Frontend

A Next.js frontend application that connects to a FastAPI backend to provide personalized shop recommendations based on user needs.

## Features

- **Smart Form**: Input fields for issue type, budget, urgency, and district
- **Real-time Recommendations**: Fetches ranked shop recommendations from the backend
- **Beautiful UI**: Modern, responsive design with Tailwind CSS
- **Rich Cards**: Detailed shop information with ratings, badges, and match indicators
- **Visual Indicators**: Badges for verified shops, district matches, and other criteria

## Setup Instructions

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- FastAPI backend running on `http://localhost:8000`

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:3000`

### Backend Setup

Make sure your FastAPI backend is running:

1. Navigate to the backend directory:
   ```bash
   cd ../backend
   ```

2. Activate your virtual environment:
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Start the FastAPI server:
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

## Usage

1. **Fill out the form** with your requirements:
   - **Issue Type**: Select from predefined options (GPU Overheat, Blue Screen, etc.)
   - **Budget**: Choose Low, Medium, or High
   - **Urgency**: Select Low, Medium, or High
   - **District**: Pick your district from the dropdown

2. **Click "Find Shops"** to get personalized recommendations

3. **Review the results**:
   - Shops are ranked by match score (0-100%)
   - Each card shows shop details, ratings, and badges
   - Look for verified shops (✅) and district matches (📍)

## API Integration

The frontend sends POST requests to `http://localhost:8000/rank_auto` with the following payload:

```json
{
  "error_type": "GPU Overheat",
  "budget": "medium",
  "urgency": "high",
  "user_district": "Colombo"
}
```

The backend returns an array of shop recommendations with detailed scoring and match information.

## Technologies Used

- **Next.js 15**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **React Hooks**: State management and side effects
- **Fetch API**: HTTP requests to backend

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Main page with form and results
│   │   └── globals.css         # Global styles
│   └── components/
│       └── RecommendationCard.tsx  # Shop recommendation card component
├── public/                     # Static assets
├── package.json               # Dependencies and scripts
└── README.md                  # This file
```

## Troubleshooting

### CORS Issues
If you encounter CORS errors, make sure your FastAPI backend has CORS middleware configured to allow requests from `http://localhost:3000`.

### Backend Not Responding
Ensure your FastAPI backend is running on port 8000 and accessible at `http://localhost:8000/rank_auto`.

### Build Issues
If you encounter build issues, try:
```bash
npm run build
npm start
```

## Customization

### Adding New Issue Types
To add new issue types, update the `errorTypes` array in `src/app/page.tsx` and ensure your backend's `ERR_TO_TYPE` mapping includes the new type.

### Styling Changes
The application uses Tailwind CSS. Modify the classes in the components to change the appearance.

### API Endpoint
To change the backend URL, update the fetch URL in the `handleSubmit` function in `src/app/page.tsx`.