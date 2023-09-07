document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Send email code triggered by submit button on form
  document.querySelector('#compose-form').addEventListener('submit', email_send); 
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email_view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email_view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


  email_box(mailbox)
  
}

// function to send an email. Form information is harvested and sent via API.
function email_send(event){
  {
    event.preventDefault();

    // Form information completed by user.
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    // Post request to send form information via API.
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
      })
    })
      .then(response => response.json())
      .then(result => {
        console.log(result);
        document.querySelector('#compose-view').style.display = 'none';
        load_mailbox('sent');
      })
      .catch(error => {
        console.error('Error sending email:', error);
      });
  };

}

// Calls API for inbox, sent, or archived mail for logged in user.
function email_box(mailbox) {
  let apiUrl = `/emails/${mailbox}`;
  fetch(apiUrl)
    .then(response => response.json())
    .then(emails => {
      if (!Array.isArray(emails)) {
        console.error('Invalid response. Expected an array of emails:', emails);
        return;
      }
      const emailsView = document.getElementById("emails-view");

      function displayEmails(emails) {
        emails.forEach((email) => {
          const emailDiv = document.createElement("div");
          emailDiv.className = email.read ? "read-email" : "unread-email";
      
          // Creates a href element for each email
          const emailLink = document.createElement("a");
          emailLink.href = "#"; // Use a placeholder link for now
          emailLink.style.textDecoration = "none";
          
          // Adds a click event listener to the email link
          emailLink.addEventListener("click", function(event) {
            event.preventDefault(); // Prevents the default link behavior
            email_view(email.id); // Calls the email_view function with the email ID
          });
      
          const emailContent = `
            <div style="border: 1px solid #ccc; padding: 10px; margin: 10px;">
              <h2>Sender: ${email.sender}</h2>
              <h3>Subject: ${email.subject}</h3>
              <h3>Date Received: ${email.timestamp}</h3>
            </div>
          `;
      
          emailLink.innerHTML = emailContent;
          emailDiv.appendChild(emailLink); // Adds link to email div
          emailsView.appendChild(emailDiv);
        });
      }
      
      // Calls function with JSON data
      displayEmails(emails);
    });
}

// function to allow user to view individual emails
function email_view(emailId) {
  // Hides the emails-view and compose-view, and show the email_view
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email_view').style.display = 'block';

  document.querySelector('#email_view').innerHTML = '';
  
  let apiURL = `/emails/${emailId}`;
  
  fetch(apiURL)
    .then(response => response.json())
    .then(email => {

      function displayEmail(email) {
        const emailDiv = document.createElement("div");
        emailDiv.innerHTML = `
          <h2>From: ${email.sender}</h2>
          <h2>Subject: ${email.subject}</h2>
          <h4>Date Received: ${email.timestamp}</h4>
          <h4>Body:</h4>
          <p>${email.body}</p>
          <br>
          <button id="archiveButton">Archive</button>
          <button id="reply">Reply</button>
        `;
        document.querySelector('#email_view').appendChild(emailDiv);

        const archiveButton = emailDiv.querySelector('#archiveButton');
        const replyButton = emailDiv.querySelector('#reply');

        
        archiveButton.addEventListener('click', () => {
          const emailArchStatues = email.archived;
          const emailId = email.id
          archiveEmail(emailId, emailArchStatues);
          load_mailbox('inbox');
        })

        replyButton.addEventListener('click', () => {
          const replyEmail = email;
          reply(email);
        })
      }

      displayEmail(email);
    })
    .catch(error => {
      console.error('Error fetching email:', error);
    });

  fetch(apiURL, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  });
}

// Function to archive or unarchive an email
function archiveEmail(emailId, emailArchStatues) {

  // When an email is set to be archived or unarchived we take the opposite value as the new
  // value for the archival status of the email.
  newArchStatus = !emailArchStatues

  let archiveAPI = `/emails/${emailId}`;
  fetch(archiveAPI, {
    method: 'PUT',
    body: JSON.stringify({
      archived: newArchStatus
    })
  })
}

function reply(email) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email_view').style.display = 'none';

  // Fill composition fields for reply
  document.querySelector('#compose-recipients').value = `${email.recipients}`;
  document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
  document.querySelector('#compose-body').value = `\n\nOn ${email.timestamp} ${email.sender} wrote: \n${email.body}`;
}
