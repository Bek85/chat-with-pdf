# 🎨 Colorful Logging Integration Guide

This guide shows how to apply the centralized colorful logging service throughout your application.

## 🚀 Quick Start

Replace any existing logging or print statements with our colorful logging service:

```python
# ❌ Old way
print("Processing started")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ New way
from app.logging import get_module_logger
logger = get_module_logger("module.name")
logger.info("Processing started")  # Appears in green!
```

## 📁 Integration Examples by Module

### 🌐 **Flask Views & Routes**

```python
# In app/web/views/pdf_views.py
from app.logging import get_module_logger

logger = get_module_logger("web.views.pdf")

@bp.route("/upload", methods=["POST"])
def upload_pdf():
    logger.info("PDF upload request received")

    try:
        # Upload logic
        logger.debug("Processing uploaded file")
        logger.info("PDF uploaded successfully")
    except Exception as e:
        logger.error(f"PDF upload failed: {str(e)}", exc_info=True)
```

### 🤖 **Chat & AI Components**

```python
# In app/chat/embeddings/openai.py
from app.logging import get_module_logger

logger = get_module_logger("chat.embeddings.openai")

def create_embeddings(text):
    logger.info("Creating OpenAI embeddings")

    try:
        # Embedding logic
        logger.debug(f"Processing {len(text)} characters")
        logger.info("Embeddings created successfully")
    except Exception as e:
        logger.error(f"Embedding creation failed: {str(e)}", exc_info=True)
```

### ⚙️ **Celery Tasks** (Already Updated)

```python
# In app/web/tasks/embeddings.py
from app.logging import get_module_logger

logger = get_module_logger("celery.tasks.embeddings")

@shared_task()
def process_document(pdf_id: int):
    logger.info(f"Starting document processing: {pdf_id}")  # Green

    try:
        # Task logic
        logger.info("Document processed successfully")  # Green
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}", exc_info=True)  # Red
```

### 🗄️ **Database Models**

```python
# In app/web/db/models/pdf.py
from app.logging import get_module_logger

logger = get_module_logger("web.db.models.pdf")

class Pdf:
    @classmethod
    def create(cls, **kwargs):
        logger.debug(f"Creating new PDF record: {kwargs.get('name', 'unknown')}")

        try:
            # Database logic
            logger.info(f"PDF record created: {instance.name}")
            return instance
        except Exception as e:
            logger.error(f"Failed to create PDF record: {str(e)}", exc_info=True)
            raise
```

### 🔧 **API Endpoints**

```python
# In app/web/api.py
from app.logging import get_module_logger

logger = get_module_logger("web.api")

def get_messages_by_conversation_id(conversation_id: str):
    logger.info(f"Fetching messages for conversation: {conversation_id}")

    try:
        messages = db.session.query(Message)...
        logger.debug(f"Found {len(messages)} messages")
        return messages
    except Exception as e:
        logger.error(f"Failed to fetch messages: {str(e)}", exc_info=True)
        raise
```

## 🎨 Color Scheme Reference

- **🔵 DEBUG** - Cyan - Detailed debugging information
- **🟢 INFO** - Green - General application flow
- **🟡 WARNING** - Yellow - Warning conditions
- **🔴 ERROR** - Red - Error conditions
- **🟣 CRITICAL** - Magenta - Critical errors

## 📝 Best Practices

### 1. **Module Naming Convention**
```python
# Use hierarchical module names that match your file structure
get_module_logger("web.views.auth")      # app/web/views/auth_views.py
get_module_logger("chat.vector_stores")  # app/chat/vector_stores/
get_module_logger("celery.tasks.email")  # app/celery/tasks/email.py
```

### 2. **Log Levels Usage**
```python
logger.debug("Detailed variable values, API responses")
logger.info("User actions, successful operations")
logger.warning("Deprecated features, fallback usage")
logger.error("Exceptions, failed operations")
logger.critical("System failures, security issues")
```

### 3. **Exception Logging**
```python
try:
    risky_operation()
except Exception as e:
    # Include exc_info=True for full stack trace
    logger.error(f"Operation failed: {str(e)}", exc_info=True)
    raise
```

### 4. **Structured Logging**
```python
logger.info("User uploaded file", extra={
    "user_id": user.id,
    "filename": file.name,
    "size": file.size
})
```

## 🔧 Configuration

### Environment Variables (in .env)
```bash
# Logging Configuration
LOG_LEVEL=INFO                    # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_CONSOLE_COLORED=true          # Enable/disable colors
LOG_CONSOLE_ENABLED=true          # Enable/disable console output
LOG_FILE_ENABLED=true             # Enable/disable file logging
LOG_FILE_PATH=logs/app.log        # Log file location
```

### Environment-Specific Configs
```python
# Development - lots of colorful debug info
LOG_LEVEL=DEBUG
LOG_CONSOLE_COLORED=true

# Production - warnings and errors only
LOG_LEVEL=WARNING
LOG_CONSOLE_COLORED=true

# Testing - minimal logging
LOG_LEVEL=ERROR
LOG_CONSOLE_COLORED=false
```

## 🚀 Already Integrated Components

✅ **Celery Workers** - Full colorful logging integration
✅ **Celery Tasks** - Replace print statements with colored logs
✅ **Flask App** - Automatic logging initialization
✅ **Pinecone Vector Store** - Using centralized logging

## 🎯 Quick Migration Checklist

For each Python file:

1. **Replace imports:**
   ```python
   # Remove
   import logging
   logging.basicConfig()
   logger = logging.getLogger(__name__)

   # Add
   from app.logging import get_module_logger
   logger = get_module_logger("your.module.name")
   ```

2. **Replace print statements:**
   ```python
   # Replace
   print(f"Processing {item}")

   # With
   logger.info(f"Processing {item}")
   ```

3. **Add exception logging:**
   ```python
   except Exception as e:
       logger.error(f"Error: {str(e)}", exc_info=True)
   ```

4. **Test the colors:**
   ```bash
   # Run your component and see the beautiful colors!
   python -m your.module
   celery -A app.celery.worker worker --loglevel=info
   ```

Now your entire application will have beautiful, consistent, colorful logging! 🎨✨