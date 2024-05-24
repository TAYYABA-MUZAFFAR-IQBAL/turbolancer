// Create the toastParent element if it doesn't exist
let toastParent = document.getElementById('toast_parent-TurboLancer');
let activeToasts = [];

function toast(type, text, padding = 0) {
  console.log('triggered...');

  // Create the toastParent if it doesn't exist
  if (!toastParent) {
    toastParent = document.createElement('div');
    toastParent.id = 'toast_parent-TurboLancer';
    document.body.appendChild(toastParent);
  }

  const toastElement = document.createElement('div');
  toastElement.classList.add('toast-TurboLancer');
  toastElement.setAttribute('role', 'alert');
  toastElement.id = type;

  const toastContent = document.createElement('div');
  toastContent.classList.add('toast-contentt');
  toastElement.appendChild(toastContent);

  const toastIcon = document.createElement('div');
  toastIcon.classList.add('toast-icont');
  toastContent.appendChild(toastIcon);

  const icon = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  icon.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
  icon.setAttribute('width', '16');
  icon.setAttribute('height', '16');
  icon.setAttribute('fill', 'currentColor');
  icon.setAttribute('viewBox', '0 0 16 16');
  toastIcon.appendChild(icon);

  const iconPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  if (type === 's') {
    iconPath.setAttribute('d', 'M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z');
  } else if (type === 'd') {
    iconPath.setAttribute('d', 'M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z');
  } else if (type === 'w') {
    iconPath.setAttribute('d', 'M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z');
  }
  icon.appendChild(iconPath);

  const toastText = document.createElement('div');
  toastText.classList.add('toasttextt');
  toastContent.appendChild(toastText);

  const textNode = document.createElement('p');
  textNode.textContent = text;
  textNode.style.paddingTop = `${padding}px`
  toastText.appendChild(textNode);

  toastParent.appendChild(toastElement);

  const toastTimeout = setTimeout(() => {
    toastElement.classList.add('go');
    setTimeout(() => {
      toastElement.classList.remove('go');
      toastElement.classList.add('none');
      toastParent.removeChild(toastElement);
      activeToasts = activeToasts.filter(t => t.element !== toastElement);

      // Remove the toastParent if it's empty
      if (!toastParent.hasChildNodes()) {
        document.body.removeChild(toastParent);
        toastParent = null;
      }
    }, 400);
  }, 4000); // Display the toast for 4 seconds

  activeToasts.push({ element: toastElement, timeout: toastTimeout });
}



function openit(x){
  const div = document.createElement('div')
    div.id='imgvp'
    document.body.appendChild(div)
    const img = x.cloneNode(true)
    img.id = '';
    img.className = ''; 
    img.onclick = null;
    
    img.style.width = 'auto';
    img.style.maxWidth = '800px';
    img.style.maxHeight = '80%';
    img.style.borderRadius = '10px';
    img.style.animation = 'showupimg 0.4s ease';
    div.appendChild(img)
    div.addEventListener('click', function() {
    this.classList.add('go')
    setTimeout(() => {
        this.remove()
    }, 400);
  });
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
window.addEventListener('DOMContentLoaded', function() {

function deleteCookie(cookieName) {
  try {
    const expirationDate = new Date(0);
    const formattedDate = expirationDate.toUTCString();
    document.cookie = `${cookieName}=; expires=${formattedDate}; path=/;`;
  } catch (error) {
    console.error(`Error deleting cookie "${cookieName}":`, error);
  }
 }
 
 function deleteCookiesAndReload(cookieNames) {
  try {
    cookieNames.forEach(deleteCookie);
    window.location.reload();
  } catch (error) {
    console.error("Error deleting cookies and reloading page:", error);
  }
 }
  const deleteButtons = document.querySelectorAll("#deleteCookieButton");

  deleteButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const cookiesToDelete = ["ideo", "emalo", "deno", "tp"];
      deleteCookiesAndReload(cookiesToDelete);
    });
  });
});
/////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////
function getMonthsArray(startMonthYear) {

  const start_date = new Date(startMonthYear);
  const current_date = new Date();
  const months_array = [];

  for (let year = start_date.getFullYear(); year <= current_date.getFullYear(); year++) {
    const endMonth = year === current_date.getFullYear() ? current_date.getMonth() : 11;
    for (let month = year === start_date.getFullYear() ? start_date.getMonth() : 0; month <= endMonth; month++) {
      const date_obj = new Date(year, month, 1);
      months_array.push(date_obj.toLocaleString('en-US', { year: 'numeric', month: 'short' }));
    }
  }
console.log(months_array)
  return months_array;
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////


const ARRAY = [
  "Web Development",
  "Mobile App Development",
  "Software Development",
  "Game Development",
  "E-commerce Development",
  "Blockchain Development",
  "Artificial Intelligence",
  "Machine Learning",
  "Data Science",
  "Data Analysis",
  "Database Administration",
  "DevOps",
  "Cloud Computing",
  "Cybersecurity",
  "UI/UX Design",
  "Graphic Design",
  "Logo Design",
  "Illustration",
  "3D Modeling",
  "Animation",
  "Video Editing",
  "Motion Graphics",
  "Photography (Editing)",
  "Photo Editing",
  "Voice Over",
  "Music Production",
  "Sound Design",
  "Content Writing",
  "Copywriting",
  "Technical Writing",
  "Blog Writing",
  "Ghostwriting",
  "Translation",
  "Transcription",
  "Proofreading",
  "Editing",
  "Digital Marketing",
  "SEO",
  "Social Media Marketing",
  "Email Marketing",
  "Content Marketing",
  "Affiliate Marketing",
  "PPC Advertising",
  "Market Research",
  "Sales Strategy",
  "Business Development",
  "Lead Generation",
  "Customer Service",
  "Virtual Assistance",
  "Project Management",
  "Product Management",
  "Business Analysis",
  "Financial Analysis",
  "Accounting",
  "Bookkeeping",
  "Consulting",
  "Legal Services",
  "HR Services",
  "Recruitment",
  "Training and Development",
  "IT Support",
  "Technical Support",
  "Network Administration",
  "System Administration",
  "ERP/CRM Management",
  "Supply Chain Management",
  "Instructional Design",
  "Corporate Training",
  "E-learning Development",
  "Online Teaching",
  "Virtual Events",
  "Webinars",
  "Podcasting",
  "Blogging",
  "Vlogging",
  "Social Media Content",
  "Infographics",
  "Email Newsletters",
  "Chatbot Development",
  "Custom Software",
  "Plugin Development",
  "API Integration",
  "Custom Scripts",
  "Automation Services",
  "Data Entry",
  "Data Mining",
  "Data Cleansing",
  "Excel Services",
  "CRM Management",
  "Lead Management",
  "Cold Calling",
  "Telemarketing",
  "Customer Surveys",
  "User Testing",
  "Product Testing",
  "Market Analysis",
  "Competitor Analysis",
  "Industry Analysis",
  "Feasibility Studies",
  "Business Plans",
  "Pitch Decks",
  "Grant Writing",
  "Proposal Writing",
  "Resume Writing",
  "LinkedIn Profile Optimization",
  "Job Application Assistance",
  "Career Counseling",
  "Interview Coaching",
  "Mock Interviews",
  "Negotiation Coaching",
  "Public Speaking Coaching",
  "Voice Coaching",
  "Accent Reduction",
  "Language Instruction",
  "ESL Instruction",
  "Curriculum Development",
  "Educational Consultation",
  "Special Education Services",
  "Event Photography (Editing)",
  "Wedding Photography (Editing)",
  "Portrait Photography (Editing)",
  "Product Photography (Editing)",
  "Food Photography (Editing)",
  "Travel Photography (Editing)",
  "Real Estate Photography (Editing)",
  "Aerial Photography (Editing)",
  "Documentary Filmmaking (Editing)",
  "Corporate Videography (Editing)",
  "Event Videography (Editing)",
  "Promotional Videos (Editing)",
  "Explainer Videos",
  "Educational Videos",
  "YouTube Channel Management",
  "Podcast Editing",
  "Audio Editing",
  "Audiobook Production",
  "Jingle Creation",
  "Music Composition",
  "Sound Effects",
  "Voice Acting",
  "Narration",
  "Dubbing",
  "Subtitling",
  "Closed Captioning",
  "Live Interpretation",
  "Medical Transcription",
  "Legal Transcription",
  "Academic Transcription",
  "Market Research Analysis",
  "Survey Design",
  "Questionnaire Design",
  "Market Segmentation",
  "Brand Positioning",
  "Consumer Behavior Analysis",
  "Trend Analysis",
  "User Research",
  "Persona Development",
  "Wireframing",
  "Prototyping",
  "User Journey Mapping",
  "Accessibility Consulting",
  "Inclusive Design",
  "Design Thinking Workshops",
  "Agile Coaching",
  "Scrum Master Services",
  "Kanban Coaching",
  "Process Improvement",
  "Change Management",
  "Risk Management",
  "Quality Assurance",
  "Testing Services",
  "User Acceptance Testing",
  "Regression Testing",
  "Performance Testing",
  "Load Testing",
  "Security Testing",
  "Usability Testing",
  "Localization Testing",
  "Localization Services",
  "Cultural Consulting",
  "Global Marketing",
  "Patent Consulting",
  "Trademark Consulting",
  "Intellectual Property Consulting"
];
function OFC(){
  return ARRAY;
}




