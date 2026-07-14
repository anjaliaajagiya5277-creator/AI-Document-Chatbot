/* ==========================================================
    AI DOCUMENT CHATBOT
    PROFESSIONAL SCRIPT
    PART 1
========================================================== */

/* ==========================================================
    APPLICATION CONFIG
========================================================== */

const CONFIG = {

    APP_NAME: "AI Document Chatbot",

    VERSION: "2.0",

    MAX_HISTORY: 10,

    MAX_TEXTAREA_HEIGHT: 180,

    CHAT_ENDPOINT: "/chat",

    CLEAR_ENDPOINT: "/clear_chat"

};

/* ==========================================================
    APPLICATION STATE
========================================================== */

const AppState = {

    isLoading: false,

    uploaded: false,

    chatCount: 0,

    currentFile: null

};

/* ==========================================================
    DOM CACHE
========================================================== */

const UI = {

    documentInput: document.getElementById("documentInput"),

    selectedFile: document.getElementById("selectedFile"),

    askButton: document.getElementById("askButton"),

    questionInput: document.getElementById("questionInput"),

    chatMessages: document.getElementById("chatMessages"),

    historyList: document.getElementById("historyList"),

    loadingOverlay: document.getElementById("loadingOverlay"),

    clearChatBtn: document.getElementById("clearChatBtn"),

    downloadTxt: document.getElementById("downloadTxt"),

    downloadPdf: document.getElementById("downloadPdf"),

    summaryText: document.getElementById("summaryText"),

    sourcesPanel: document.getElementById("sourcesPanel"),

    chatCounter: document.getElementById("chatCounter")

};

/* ==========================================================
    COMMON HELPERS
========================================================== */

function escapeHTML(text){

    if(text === null || text === undefined){

        return "";

    }

    return String(text)

        .replace(/&/g,"&amp;")

        .replace(/</g,"&lt;")

        .replace(/>/g,"&gt;")

        .replace(/"/g,"&quot;")

        .replace(/'/g,"&#039;");

}

function getCurrentTime(){

    return new Date().toLocaleTimeString(

        [],

        {

            hour:"2-digit",

            minute:"2-digit"

        }

    );

}

function scrollChatToBottom(){

    if(!UI.chatMessages){

        return;

    }

    UI.chatMessages.scrollTop =

        UI.chatMessages.scrollHeight;

}

function removeWelcomeMessage(){

    const welcome =

        UI.chatMessages.querySelector(

            ".welcome-message"

        );

    if(welcome){

        welcome.remove();

    }

}

/* ==========================================================
    LOADING OVERLAY
========================================================== */

function showLoadingOverlay(){

    if(UI.loadingOverlay){

        UI.loadingOverlay.style.display = "flex";

    }

}

function hideLoadingOverlay(){

    if(UI.loadingOverlay){

        UI.loadingOverlay.style.display = "none";

    }

}

/* ==========================================================
    ASK BUTTON STATE
========================================================== */

function setLoading(status){

    AppState.isLoading = status;

    if(UI.askButton){

        UI.askButton.disabled = status;

        UI.askButton.innerHTML =

            status

            ? "Thinking..."

            : "Ask AI";

    }

    if(UI.questionInput){

        UI.questionInput.disabled = status;

    }

}

/* ==========================================================
    FILE UPLOAD PREVIEW
========================================================== */

if(UI.documentInput){

    UI.documentInput.addEventListener(

        "change",

        function(){

            if(this.files.length){

                AppState.uploaded = true;

                AppState.currentFile =

                    this.files[0].name;

                UI.selectedFile.innerHTML =

                    "✅ " +

                    this.files[0].name;

            }

            else{

                AppState.uploaded = false;

                AppState.currentFile = null;

                UI.selectedFile.innerHTML =

                    "PDF / PPT / PPTX";

            }

        }

    );

}

/* ==========================================================
    AUTO RESIZE TEXTAREA
========================================================== */

if(UI.questionInput){

    UI.questionInput.addEventListener(

        "input",

        function(){

            this.style.height = "auto";

            this.style.height =

                Math.min(

                    this.scrollHeight,

                    CONFIG.MAX_TEXTAREA_HEIGHT

                ) + "px";

        }

    );

}

/* ==========================================================
    AUTO SCROLL OBSERVER
========================================================== */

if(UI.chatMessages){

    const observer =

        new MutationObserver(function(){

            scrollChatToBottom();

        });

    observer.observe(

        UI.chatMessages,

        {

            childList:true

        }

    );

}

/* ==========================================================
    TOAST
========================================================== */

function showToast(message){

    const old =

        document.querySelector(".toast");

    if(old){

        old.remove();

    }

    const toast =

        document.createElement("div");

    toast.className =

        "toast fade-in";

    toast.innerHTML = message;

    document.body.appendChild(toast);

    setTimeout(function(){

        toast.remove();

    },2500);

}

/* ==========================================================
    APPLICATION STARTUP
========================================================== */

window.addEventListener(

    "load",

    function(){

        if(UI.chatCounter){

            UI.chatCounter.innerHTML =

                "Questions : 0";

        }

        console.log(

            CONFIG.APP_NAME +

            " Loaded"

        );

    }

);
/* ==========================================================
    PART 2
    CHAT ENGINE
========================================================== */

/* ==========================================================
    FORMAT AI RESPONSE
========================================================== */

function formatAIResponse(text){

    if(!text){

        return "";

    }

    text = escapeHTML(text);

    text = text.replace(

        /```([\s\S]*?)```/g,

        "<pre><code>$1</code></pre>"

    );

    text = text.replace(

        /`([^`]+)`/g,

        "<code>$1</code>"

    );

    text = text.replace(

        /\*\*(.*?)\*\*/g,

        "<strong>$1</strong>"

    );

    text = text.replace(

        /^(\d+)\.\s(.*)$/gm,

        "<strong>$1.</strong> $2"

    );

    text = text.replace(

        /^\*\s(.*)$/gm,

        "• $1"

    );

    text = text.replace(

        /\n/g,

        "<br>"

    );

    return text;

}

/* ==========================================================
    USER MESSAGE
========================================================== */
function addUserMessage(message){

    removeWelcomeMessage();

    const html = `

        <div class="user-message fade-in">

            <div class="message-content">

                <div class="message-header">

                    👤 You

                    <span class="message-time">

                        ${getCurrentTime()}

                    </span>

                </div>

                <div class="message-body">

                    ${escapeHTML(message)}

                </div>

            </div>

        </div>

    `;

    UI.chatMessages.insertAdjacentHTML(

        "beforeend",

        html

    );

    scrollChatToBottom();

}
/* ==========================================================
    TYPING INDICATOR
========================================================== */

function showTypingIndicator(){

    removeWelcomeMessage();

    UI.chatMessages.insertAdjacentHTML(

        "beforeend",

        `

        <div
            id="typingIndicator"
            class="ai-message fade-in">

            <div class="message-avatar">

                🤖

            </div>

            <div class="message-content">

                <div class="typing">

                    <span></span>

                    <span></span>

                    <span></span>

                </div>

                <small>

                    AI is thinking...

                </small>

            </div>

        </div>

        `

    );

}

function hideTypingIndicator(){

    const typing =

        document.getElementById(

            "typingIndicator"

        );

    if(typing){

        typing.remove();

    }

}

/* ==========================================================
    UPDATE SOURCES PANEL
========================================================== */

function updateSourcesPanel(sources){

    if(!UI.sourcesPanel){

        return;

    }

    if(!sources || !sources.length){

        UI.sourcesPanel.innerHTML =

            `<div class="empty-source">

                No sources available.

            </div>`;

        return;

    }

    let html = "";

    sources.forEach(source=>{

        html += `

        <div class="source-card">

            <div>

                <strong>

                    📄 ${escapeHTML(source.source || "Document")}

                </strong>

            </div>

            <div>

                Chunk :
                ${source.chunk_id ?? "-"}

            </div>

            ${source.page ? `<div>Page : ${source.page}</div>` : ""}

            ${source.slide ? `<div>Slide : ${source.slide}</div>` : ""}

        </div>

        `;

    });

    UI.sourcesPanel.innerHTML = html;

}

/* ==========================================================
    AI MESSAGE
========================================================== */

function addAIMessage(answer, sources=[]){

    removeWelcomeMessage();


    UI.chatMessages.insertAdjacentHTML(

        "beforeend",

        `

        <div class="ai-message fade-in">

            <div class="message-avatar">

                🤖

            </div>

            <div class="message-content">

                <div class="message-header">

                    AI Assistant

                    <span class="message-time">

                        ${getCurrentTime()}

                    </span>

                </div>

                <div class="message-body">

                    ${formatAIResponse(answer)}

                </div>

                <div class="response-actions">

                    <button class="copy-btn">

                        📋 Copy

                    </button>

                    <button class="feedback-btn like-btn">

                        👍 Helpful

                    </button>

                    <button class="feedback-btn dislike-btn">

                        👎 Not Helpful

                    </button>

                </div>

            </div>

        </div>

        `

    );

    attachCopyEvents();

    attachFeedbackEvents();

    saveChatHistory();

    updateSourcesPanel(sources);

    updateStatistics();

    updateProcessingStatus();

    scrollChatToBottom();

}

/* ==========================================================
    SEND QUESTION
========================================================== */

async function sendQuestion(){

    if(AppState.isLoading){

        return;

    }

    const question =

        UI.questionInput.value.trim();

    if(question===""){

        showToast(

            "Please enter a question."

        );

        UI.questionInput.focus();

        return;

    }

    addUserMessage(question);

    addHistory(question);

    UI.questionInput.value="";

    UI.questionInput.style.height="auto";

    showTypingIndicator();

    setLoading(true);

    try{

        const response = await fetch(

            CONFIG.CHAT_ENDPOINT,

            {

                method:"POST",

                headers:{

                    "Content-Type":"application/json"

                },

                body:JSON.stringify({

                    question:question

                })

            }

        );

        const data = await response.json();

        hideTypingIndicator();

        if(data.success){

            addAIMessage(

                data.answer,

                data.sources || []

            );

            AppState.chatCount=data.chat_count || AppState.chatCount+1;

if(UI.chatCounter){

    UI.chatCounter.innerHTML=

        "Questions : "

        + AppState.chatCount;

}

        }

        else{

            addAIMessage(

                "❌ " +

                data.message,

                []

            );

        }

    }

    catch(error){

        hideTypingIndicator();

        console.error(error);

        addAIMessage(

            "⚠ Unable to connect to the server."

        );

    }

    finally{

        setLoading(false);

    }

}
/* ==========================================================
    PART 3
    CHAT UTILITIES
========================================================== */

/* ==========================================================
    CONVERSATION HISTORY
========================================================== */

function addHistory(question){

    if(!UI.historyList){

        return;

    }

    const empty = UI.historyList.querySelector(

        ".history-empty"

    );

    if(empty){

        empty.remove();

    }

    const item = document.createElement("div");

    item.className = "history-item";

    item.innerHTML = `

        <div class="history-question">

            ${escapeHTML(question)}

        </div>

        <div class="history-time">

            ${getCurrentTime()}

        </div>

    `;

    item.onclick = function(){

        UI.questionInput.value = question;

        UI.questionInput.focus();

    };

    UI.historyList.prepend(item);

    while(

        UI.historyList.children.length >

        CONFIG.MAX_HISTORY

    ){

        UI.historyList.removeChild(

            UI.historyList.lastChild

        );

    }

}

/* ==========================================================
    COPY RESPONSE
========================================================== */

function attachCopyEvents(){

    document

        .querySelectorAll(".copy-btn")

        .forEach(button=>{

            button.onclick = function(){

                const text = this

                    .closest(".message-content")

                    .querySelector(".message-body")

                    .innerText;

                navigator.clipboard

                    .writeText(text)

                    .then(()=>{

                        const old = this.innerHTML;

                        this.innerHTML = "✅ Copied";

                        showToast(

                            "Response copied."

                        );

                        setTimeout(()=>{

                            this.innerHTML = old;

                        },1500);

                    });

            };

        });

}

/* ==========================================================
    FEEDBACK
========================================================== */

function attachFeedbackEvents(){

    document

        .querySelectorAll(".like-btn")

        .forEach(button=>{

            button.onclick = function(){

                this.disabled = true;

                const dislike =

                    this.parentElement

                    .querySelector(

                        ".dislike-btn"

                    );

                if(dislike){

                    dislike.disabled = true;

                }

                this.innerHTML =

                    "✅ Thanks";

            };

        });

    document

        .querySelectorAll(".dislike-btn")

        .forEach(button=>{

            button.onclick = function(){

                this.disabled = true;

                const like =

                    this.parentElement

                    .querySelector(

                        ".like-btn"

                    );

                if(like){

                    like.disabled = true;

                }

                this.innerHTML =

                    "📝 Recorded";

            };

        });

}

/* ==========================================================
    SAVE CHAT
========================================================== */

function saveChatHistory(){

    if(!UI.chatMessages){

        return;

    }

    sessionStorage.setItem(

        "chatHistory",

        UI.chatMessages.innerHTML

    );

}

/* ==========================================================
    RESTORE CHAT
========================================================== */

function restoreChatHistory(){

    const history =

        sessionStorage.getItem(

            "chatHistory"

        );

    if(

        history &&

        UI.chatMessages

    ){

        UI.chatMessages.innerHTML = history;

        attachCopyEvents();

        attachFeedbackEvents();

    }

}

/* ==========================================================
    CHAT EXPORT
========================================================== */

function getChatText(){

    let text = "";

    document

        .querySelectorAll(

            ".user-message,.ai-message"

        )

        .forEach(message=>{

            text +=

                message.innerText +

                "\n\n---------------------------------\n\n";

        });

    return text;

}

/* ==========================================================
    DOWNLOAD TXT
========================================================== */

if(UI.downloadTxt){

    UI.downloadTxt.addEventListener(

        "click",

        function(){

            const blob =

                new Blob(

                    [getChatText()],

                    {

                        type:"text/plain"

                    }

                );

            const url =

                URL.createObjectURL(blob);

            const a =

                document.createElement("a");

            a.href = url;

            a.download =

                "AI_Document_Chat.txt";

            a.click();

            URL.revokeObjectURL(url);

        }

    );

}

/* ==========================================================
    DOWNLOAD PDF
========================================================== */

if(UI.downloadPdf){

    UI.downloadPdf.addEventListener(

        "click",

        function(){

            window.print();

        }

    );

}

/* ==========================================================
    CLEAR CHAT
========================================================== */

if(UI.clearChatBtn){

    UI.clearChatBtn.addEventListener(

        "click",

        async function(){

            try{

                const response =

                    await fetch(

                        CONFIG.CLEAR_ENDPOINT,

                        {

                            method:"POST"

                        }

                    );

                const data =

                    await response.json();

                if(data.success){

                    sessionStorage.removeItem(

                        "chatHistory"

                    );

                    AppState.chatCount = 0;

                    if(UI.chatCounter){

                        UI.chatCounter.innerHTML =

                            "Questions : 0";

                    }

                    UI.chatMessages.innerHTML = `

                        <div class="welcome-message">

                            <div class="welcome-icon">

                                🤖

                            </div>

                            <h2>

                                Conversation Cleared

                            </h2>

                            <p>

                                Ask another question.

                            </p>

                        </div>

                    `;

                    if(UI.historyList){

                        UI.historyList.innerHTML =

                        `

                        <div class="history-empty">

                            No conversations yet

                        </div>

                        `;

                    }

                    if(UI.sourcesPanel){

                        UI.sourcesPanel.innerHTML =

                        `

                        <div class="empty-source">

                            Sources will appear here.

                        </div>

                        `;

                    }

                    showToast(

                        "Conversation cleared."

                    );

                }

            }

            catch(error){

                console.error(error);

                showToast(

                    "Unable to clear chat."

                );

            }

        }

    );

}


/* ==========================================================
    PART 4
    FINAL INITIALIZATION
========================================================== */

/* ==========================================================
    ASK BUTTON
========================================================== */

if(UI.askButton){

    UI.askButton.addEventListener(

        "click",

        function(){

            sendQuestion();

        }

    );

}

/* ==========================================================
    ENTER TO SEND
========================================================== */

if(UI.questionInput){

    UI.questionInput.addEventListener(

        "keydown",

        function(event){

            if(

                event.key==="Enter"

                &&

                !event.shiftKey

            ){

                event.preventDefault();

                sendQuestion();

            }

        }

    );

}

/* ==========================================================
    SUGGESTED QUESTIONS
========================================================== */

document

    .querySelectorAll(".suggestion-btn")

    .forEach(button=>{

        button.addEventListener(

            "click",

            function(){

                UI.questionInput.value =

                    this.innerText;

                sendQuestion();

            }

        );

    });

/* ==========================================================
    AUTO FOCUS
========================================================== */

window.addEventListener(

    "load",

    function(){

        if(UI.questionInput){

            UI.questionInput.focus();

        }

    }

);
/*==========================================================
PHASE 6.4
RIGHT PANEL CONTROLLER
==========================================================*/



/*==========================================================
SOURCES PANEL
==========================================================*/

function updateSourcesPanel(sources){

    const panel=document.getElementById("sourcesPanel");

    if(!panel){

        return;

    }

    if(!sources || sources.length===0){

        panel.innerHTML=`

            <div class="empty-source">

                No sources available.

            </div>

        `;

        return;

    }

    panel.innerHTML="";

    sources.forEach(source=>{

        panel.innerHTML+=`

        <div class="source-card">

            <div class="source-title">

                📄 ${source.source || "Document"}

            </div>

            <div class="source-meta">

                ${source.page ? "Page "+source.page : ""}

                ${source.slide ? " Slide "+source.slide : ""}

            </div>

            <div class="source-preview">

                ${source.preview || ""}

            </div>

        </div>

        `;

    });

}



/*==========================================================
STATISTICS
==========================================================*/

function updateStatistics(){

    const stats=document.querySelectorAll(".stat-box h2");

    if(stats.length<4){

        return;

    }

    stats[3].innerHTML="Active";

}



/*==========================================================
PROCESS STATUS
==========================================================*/

function updateProcessingStatus(){

    document

    .querySelectorAll(".status-row .pending")

    .forEach(item=>{

        item.classList.remove("pending");

        item.classList.add("done");

        item.innerHTML="✔";

    });

}
/* ==========================================================
    RESTORE PREVIOUS CHAT
========================================================== */

window.addEventListener(

    "load",

    function(){

        restoreChatHistory();

    }

);

/* ==========================================================
    NETWORK STATUS
========================================================== */

window.addEventListener(

    "offline",

    function(){

        showToast(

            "⚠ Internet connection lost."

        );

    }

);

window.addEventListener(

    "online",

    function(){

        showToast(

            "✅ Internet connected."

        );

    }

);

/* ==========================================================
    GLOBAL ERROR HANDLER
========================================================== */

window.addEventListener(

    "error",

    function(event){

        console.error(

            event.error

        );

    }

);

/* ==========================================================
    APPLICATION READY
========================================================== */

window.addEventListener(

    "load",

    function(){

        console.log(

            "===================================="

        );

        console.log(

            CONFIG.APP_NAME

        );

        console.log(

            "Version :", CONFIG.VERSION

        );

        console.log(

            "Application Loaded Successfully"

        );

        console.log(

            "===================================="

        );

    }

);

/* ==========================================================
    OPTIONAL LOADING OVERLAY
========================================================== */

window.addEventListener(

    "beforeunload",

    function(){

        showLoadingOverlay();

    }

);

window.addEventListener(

    "pageshow",

    function(){

        hideLoadingOverlay();

    }

);

/* ==========================================================
    INITIAL SOURCES PANEL
========================================================== */

if(

    UI.sourcesPanel

    &&

    UI.sourcesPanel.innerHTML.trim()===""

){

    UI.sourcesPanel.innerHTML=`

        <div class="empty-source">

            Sources will appear after asking a question.

        </div>

    `;

}

/* ==========================================================
    INITIAL HISTORY PANEL
========================================================== */

if(

    UI.historyList

    &&

    UI.historyList.innerHTML.trim()===""

){

    UI.historyList.innerHTML=`

        <div class="history-empty">

            No conversations yet

        </div>

    `;

}

/* ==========================================================
    FINISHED
========================================================== */

console.log(

    "AI Document Chatbot Ready 🚀"

);