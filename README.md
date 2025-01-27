## Project Overview

**Pop Academy** is designed to provide insights into how popular songs are across different streaming platforms, offering both individual song analysis and side-by-side comparison modes. It calculates popularity based on metrics from platforms such as:

- **YouTube** (views, likes, comments)
- **Spotify** (popularity score)
- **Last.fm** (listeners, playcount)

The app allows users to compare songs using a **sortable table** of metrics and generate detailed reports.

## Features

### 1. **Song Popularity Analysis**
   - Retrieve metrics such as **YouTube views**, likes, comments, **Spotify popularity score**, and **Last.fm listeners** and playcount.
   - Generate reports on individual songs.

### 2. **Song Comparison**
   - Compare multiple songs by inputting the number of songs.
   - View popularity metrics in a **sortable table**.

### 3. **Responsive UI**
   - Mobile-friendly UI with responsive tables, modals, and buttons.
   - Pages for report cards and talent show modes.

### 4. **Custom Modal Pages**
   - Paginated modal windows to display results.
   - Report cards are presented in a clean, paginated interface, allowing users to navigate through the data.

## Tech Stack

### Frontend
- **HTML5**
- **CSS3** (with Bootstrap for layout and modals)
- **JavaScript** (for dynamic form generation, AJAX requests, and sortable tables)

### Backend
- **Python 3.8.7** (with Flask for handling server-side logic)
- **Flask-CORS**: For handling CORS between frontend and backend.

### Libraries and Tools
- **Bootstrap 5**: For responsive design and modal components.
- **FuzzyWuzzy**: For matching user inputted song names to database entries.
- **Prettier**: For code formatting.

## Demo Link:
- https://popacademy-stevens-projects.vercel.app/
