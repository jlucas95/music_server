
function addNotification(className, text){
    var notificationList = document.getElementById("notifications");
    var notification = document.createElement("li");
    notification.className = "fade list-group-item list-group-item-" + className;
    notification.innerText = text;
    notification.addEventListener("animationend", function(event){
        var parent = event.target.parentNode;
        parent.removeChild(event.target);
        });
    notificationList.appendChild(notification);
}

// Make the notificationList
var notifications = document.createElement("ul");
notifications.className = "list-group";
notifications.id = "notifications";
notifications.style.position = "fixed";
notifications.style.bottom = "10px";
notifications.style.right= "10px";
document.body.appendChild(notifications);

