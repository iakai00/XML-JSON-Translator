# Test the languages endpoint
curl -v "http://localhost:8000/api/v1/translate/languages?service_type=claude"

# Test translation with a small sample file
echo "<TEXT id=\"test\">Hello World</TEXT>" > test.xml
curl -v -X POST \
  "http://localhost:8000/api/v1/translate/xml" \
  -F "file=@test.xml" \
  -F "target_language=fi" \
  -F "service_type=claude" \
  -o translated.xml
cat translated.xml