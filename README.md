# DAIR-3
The file JSONSummaryCreation.py creates a summary of all forms. 

The file JSONEditor.py allows review and edition of the file JHS.JSON 

**Git protocol:**

After you make your changes: 
```bash
git pull
git add .
git commit -m "[description of the change]"
git push
```
Follow this protocol to make changes to the repository. 

If you need to log into git, use: 
```bash
  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"
```
If you need to cancel a git add operation, use: 
```bash
git reset 
``` 
If you need to force a retrieval of files on the server and ovewrite local changes, use: 
```bash
git reset --hard HEAD
``` 
### Prerequisites
- API key. Load the key in an environmental variables called OPENAI_API_KEY, ANTHROPIC_API_KEY and GROQ_API_KEY. 

### Installation
Simply clone or download the repository to your local machine. Execute the script. 
