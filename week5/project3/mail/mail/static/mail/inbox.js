document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Send email code triggered by submit button on form
  document.querySelector('#compose-form').addEventListener('submit', email_send) 

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


  email_box(mailbox)
  
}

function email_send(event){
  {
    event.preventDefault();

    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

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

          const emailContent = `
            <div style="border: 1px solid #ccc; padding: 10px; margin: 10px;">
              <h2>From: ${email.sender}</h2>
              <h3>Subject: ${email.subject}</h3>
              <h3>Date Received: ${email.timestamp}</h3>
            </div>
          `;

          emailDiv.innerHTML = emailContent;
          emailsView.appendChild(emailDiv);
        });
      }

      // Calls function with JSON data
      displayEmails(emails);
    })
    
}
