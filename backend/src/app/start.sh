# Run server
echo "Starting development server..."
exec uvicorn "app.main:app" --reload
