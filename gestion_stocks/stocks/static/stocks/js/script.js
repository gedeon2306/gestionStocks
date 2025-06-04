// Éléments du DOM
const hamburger = document.querySelector('.hamburger');
const navContent = document.querySelector('.nav-content');
const body = document.body;
const profileTrigger = document.querySelector('.profile-trigger');
const dropdownMenu = document.querySelector('.dropdown-menu');
const profileDropdown = document.querySelector('.profile-dropdown');

// États
let isDropdownOpen = false;
let isClickOpen = false;

// Gestion du menu hamburger
hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navContent.classList.toggle('active');
    body.style.overflow = navContent.classList.contains('active') ? 'hidden' : '';
});

// Gestion du dropdown du profil
// Ouvrir au survol
profileDropdown.addEventListener('mouseenter', () => {
    if (!isClickOpen) {
        openDropdown();
    }
});

profileDropdown.addEventListener('mouseleave', () => {
    if (!isClickOpen) {
        closeDropdown();
    }
});

// Ouvrir/Fermer au clic
profileTrigger.addEventListener('click', (e) => {
    e.stopPropagation();
    if (isClickOpen) {
        isClickOpen = false;
        closeDropdown();
    } else {
        isClickOpen = true;
        openDropdown();
    }
});

// Fermer le dropdown en cliquant en dehors
document.addEventListener('click', (e) => {
    if (!e.target.closest('.profile-dropdown') && isDropdownOpen) {
        isClickOpen = false;
        closeDropdown();
    }
});

// Fonction pour ouvrir le dropdown
function openDropdown() {
    isDropdownOpen = true;
    dropdownMenu.classList.add('active');
    dropdownMenu.style.opacity = '1';
    dropdownMenu.style.visibility = 'visible';
    if (window.innerWidth > 768) {
        dropdownMenu.style.transform = 'translateY(0)';
    } else {
        dropdownMenu.style.transform = 'translate(-50%, -50%) scale(1)';
    }
}

// Fonction pour fermer le dropdown
function closeDropdown() {
    isDropdownOpen = false;
    dropdownMenu.classList.remove('active');
    if (window.innerWidth > 768) {
        dropdownMenu.style.opacity = '0';
        dropdownMenu.style.visibility = 'hidden';
        dropdownMenu.style.transform = 'translateY(-10px)';
    } else {
        dropdownMenu.style.opacity = '0';
        dropdownMenu.style.visibility = 'hidden';
        dropdownMenu.style.transform = 'translate(-50%, -50%) scale(0.8)';
    }
}

window.addEventListener("scroll", () => {
  const element = document.querySelector(".dashboard-grid");
  const positionElement = element.getBoundingClientRect().top;
  const positionViewport = window.innerHeight / 1.3;

  if (positionElement < positionViewport) {
    element.classList.add("apparait");
  }
});

// Gestion de la recherche
function recherche() {
    // Déclare les variables
    var input, filter, table, tr, td, i, j, txtValue;
    input = document.getElementById("searchInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
  
    // Parcourt toutes les lignes du tableau (sauf l'en-tête)
    for (i = 1; i < tr.length; i++) {
        tr[i].style.display = "none"; // Masque la ligne par défaut
        td = tr[i].getElementsByTagName("td");
        // Parcourt toutes les colonnes de la ligne
        for (j = 0; j < td.length; j++) {
            if (td[j]) {
                txtValue = td[j].textContent || td[j].innerText;
                // Si une colonne correspond au filtre, affiche la ligne
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                    break; // Arrête la vérification pour cette ligne
                }
            }
        }
    }
}

// Gestion de la modification du profil (si on est sur la page edit-profile)
const editProfileForm = document.getElementById('edit-profile-form');
const profilePhotoInput = document.getElementById('profile-photo');
const changePhotoBtn = document.querySelector('.change-photo-btn');
const togglePasswordBtns = document.querySelectorAll('.toggle-password');

if (editProfileForm) {
    // Gestion du changement de photo
    if (changePhotoBtn) {
        changePhotoBtn.addEventListener('click', () => {
            profilePhotoInput.click();
        });

        profilePhotoInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.querySelector('.profile-img-container .profile-img-large').src = e.target.result;
                    document.querySelector('.profile-trigger .profile-img').src = e.target.result;
                    document.querySelector('.profile-header-content .profile-img-large').src = e.target.result;
                }
                reader.readAsDataURL(file);
            }
        });
    }

    // Gestion de l'affichage/masquage des mots de passe
    togglePasswordBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const input = e.currentTarget.parentNode.querySelector('input');
            const icon = e.currentTarget.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });
}