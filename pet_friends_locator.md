Locators for http://petfriends1.herokuapp.com/all_pets

Element      | CSS          | XPath
-------------|--------------|-------------
Header |.navbar-light | /html//nav
Header logo | a.header2 | //nav/a[@href="/"]
Navigation bar items | 1. a.nav-link[href="/my_pets"] | //li/a[@href="/my_pets"]
 _ | 2. a.nav-link[href="/all_pets"] | //li/a[@href="/all_pets"]
"Exit" button | .btn-outline-secondary | //div/button[contains(@class, "btn-outline-secondary")]
Title | head > title | //head/title
Pet card | .card-deck > .card | //div[@class="card"]
Pet photo | .card-deck img.card-img-top | //img[contains(concat(" ", @class, " "), "card-img-top")]
Pet name | .card-body h5.card-title | //div/h5[@class="card-title"]
Pet breed and age | .card-body .card-text | //p[contains(concat(" ", @class, " "), "card-text")]
