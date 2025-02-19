
document.querySelector('.search-btn').addEventListener('click', function() {
    document.querySelector('.search-input').focus();
});

const themeToggle = document.getElementById('themeToggle');
themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
});

// Automatically hide flash messages after 2 seconds
const flashMessages = document.querySelectorAll('.flash');
flashMessages.forEach(message => {
    setTimeout(() => {
        message.style.display = 'none';
    }, 2000);  // 2 seconds
});

// Mood Indicator Update
const moodIndicator = document.querySelector('.mood-indicator');
const moods = [
    {emoji: '😊', text: 'Feeling productive today!'},
    {emoji: '🚀', text: 'Ready to innovate!'},
    {emoji: '💡', text: 'Having creative ideas!'},
    {emoji: '👩‍💻', text: 'Deep in code!'},
    {emoji: '🤝', text: 'Looking to collaborate!'}
];

function updateMood() {
    const randomMood = moods[Math.floor(Math.random() * moods.length)];
    moodIndicator.innerHTML = `${randomMood.emoji} ${randomMood.text}`;
}

// Update mood indicator every 5 seconds
setInterval(updateMood, 5000);

// Initial mood update on page load
updateMood();