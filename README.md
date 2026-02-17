<<<<<<< HEAD

#  World Rush (v0.41)

Un jeu d'association d'idées rapide et compétitif, jouable en local ou en ligne.

##  Nouveautés de la version 0.4
- **Système de "Gel du Temps"** : Achetez des charges et figez le chronomètre pendant 5 secondes !
- **Nouveaux Packs de Mots** : Jeux Vidéo, Nourriture, Super-Héros, Horreur.
- **Mode Développeur Amélioré** : Interface visuelle et nouvelles commandes de test.
- **Améliorations Visuelles** : Confettis de victoire, sons de frappe, interface magasin revue.
- **Stabilité Réseau** : Optimisation de la latence (TCP_NODELAY).

##  Modes de Jeu
- **NORMAL** : Le mode classique.
- **SURVIE** : Le temps diminue à chaque tour.
- **SPEED** : Seulement 3 secondes pour répondre !
- **HARDCORE** : 4 secondes, pas de droit à l'erreur.
- **CHAOS** : Temps aléatoire imprévisible.

##  Comment Jouer
1. **Principe** : Trouvez un mot en lien avec le précédent avant la fin du chrono.
2. **Combo** : Répondez en moins de 2.5s pour multiplier vos gains et enflammer l'écran !
3. **Contestation** : Si un mot est douteux, appuyez sur `Maj` ou `Tab` pour lancer un vote.
4. **Bonus** :
   - **Wizz** (`Ctrl + B`) : Faites trembler l'écran de l'adversaire.
   - **Gel** (Bouton ❄️) : Arrête le temps (nécessite l'objet "Stock Gel Temps").

##  Multijoueur & Social
- **En Ligne** : Hébergez une partie (UPnP automatique pour ouvrir les ports) ou rejoignez via IP.
- **Amis** : Ajoutez des joueurs, rejoignez-les facilement via le menu Amis.
- **Échanges** : Échangez des pièces et des objets avec vos amis dans le lobby d'échange.
- **Chat** : Discutez dans le lobby avant la partie.

##  Boutique & Personnalisation
- **Avatars** : Choisissez parmi les emojis ou importez votre propre image (crop intégré).
- **Cosmétiques** : 
  - Bordures animées (Rainbow, Néon, Feu...).
  - Thèmes d'interface (Matrix, Cyber, Océan...).
  - Couleurs de pseudo.
- **Packs de Mots** : Achetez de nouvelles catégories pour varier les parties.
- **Cadeau du Jour** : Récupérez des pièces gratuites chaque jour dans le magasin.

##  Sauvegarde
- Vos données (Niveau, Inventaire, Amis, Historique) sont sauvegardées automatiquement dans `world_rush_settings.json`.
- Possibilité d'exporter/importer votre sauvegarde via les Paramètres.

## Fonctionnalités

*   **Multijoueur** : Local (même PC) ou En Ligne (TCP/IP).
*   **Réseau** : Système de Lobby, Chat intégré et tentative UPnP automatique pour l'hébergement.
*   **Gameplay** : Chronomètre stressant, validation de mots, et système de contestation.
*   **Personnalisation** : Choix des thèmes, du temps et du score.
*   **succes**: permet de gagner des piece
*   **magazins** : permet d'echeter des decorations

## Contrôles

*   **Entrée** : Valider un mot / Envoyer un message.
*   **Maj (Shift)** : Contester une réponse (Configurable).
*   **Espace** : Passer au tour suivant (Mode Vocal).
=======
---
*Développé avec Python & Pygame.*

=======
# World Rush (v0.42) - Saison 1

Un jeu d'association d'idées rapide et compétitif, jouable en local ou en ligne.

##  Nouveautés de la version 0.42

### 🎨 Redesign & Personnalisation
- **Redesign Total** : Nouvelle interface utilisateur plus moderne et fluide.
- **Personnalisation Avancée** : Créez votre propre couleur de bordure ou de pseudo pour 5000 pièces !
- **Cosmétiques Animés** : Nouvelles bordures et couleurs de pseudo animées.
- **Système de Rareté** : Les objets ont maintenant des niveaux de rareté.
- **Badges** : Affichez un badge à côté de votre pseudo.
- **Catégories Personnalisées** : Créez vos propres listes de mots dans les paramètres !
- **Titres de Joueur** : Gagnez des titres évolutifs selon votre niveau.

### 🕹️ Gameplay & Modes
- **Nouveau Mode : Contre-la-montre** : Un chrono global de 60s !
- **Mode Entraînement Amélioré** : Jouez contre un Bot avec 3 niveaux de difficulté (Facile, Moyen, Difficile).
- **Battle Pass** : Progressez dans les niveaux pour débloquer des récompenses.
- **Défi du Jour** : Un défi quotidien pour gagner plus de pièces.
- **Roue de la Fortune** : Tentez votre chance chaque jour dans le magasin.
- **Succès** : De nombreux nouveaux succès à débloquer.
- **Mini-Jeu Caché** : Tapez le code `SNAKE` dans le menu Code Cadeau.
- **Plus d'objets** : Le magasin a été considérablement agrandi.

### 🌐 Multijoueur & Social
- **Stabilité Renforcée** : Ajout d'amis plus robuste et mode en ligne optimisé.
- **Ping** : Affichage de la latence dans le salon d'attente.
- **Chat Amélioré** : Ajout d'emojis et de la commande `/help`.
- **Code Cadeau** : Système de codes bonus dans les paramètres.

### 🛠️ Divers
- **Barre d'Infos** : Bandeau défilant avec astuces et infos.
- **Langue** : Option pour changer la langue (FR/EN - Test).
- **Animation de Démarrage** : Intro améliorée.
- **Secret** : Un secret a été caché... saurez-vous le trouver ?
- **Corrections de Bugs** : Nombreux correctifs.

##  Modes de Jeu
- **NORMAL** : Le mode classique.
- **SURVIE** : Le temps diminue à chaque tour.
- **SPEED** : Seulement 3 secondes pour répondre !
- **HARDCORE** : 4 secondes, pas de droit à l'erreur.
- **CHAOS** : Temps aléatoire imprévisible.
- **CONTRE-LA-MONTRE** : Course contre le temps global.

##  Comment Jouer
1. **Principe** : Trouvez un mot en lien avec le précédent avant la fin du chrono.
2. **Combo** : Répondez en moins de 2.5s pour multiplier vos gains et enflammer l'écran !
3. **Contestation** : Si un mot est douteux, appuyez sur `Maj` ou `Tab` pour lancer un vote.
4. **Entraînement** : Affrontez un Bot pour vous exercer. Réglez sa difficulté dans le menu de configuration.
5. **Bonus** :
   - **Wizz** (`Ctrl + B`) : Faites trembler l'écran de l'adversaire.
   - **Gel** (Bouton ❄️) : Arrête le temps (nécessite l'objet "Stock Gel Temps").

##  Multijoueur & Social
- **En Ligne** : Hébergez une partie (UPnP automatique pour ouvrir les ports) ou rejoignez via IP.
- **Amis** : Ajoutez des joueurs, rejoignez-les facilement via le menu Amis.
- **Échanges** : Échangez des pièces et des objets avec vos amis dans le lobby d'échange.
- **Chat** : Discutez dans le lobby. Utilisez `/help` pour voir les commandes.

##  Boutique & Personnalisation
- **Avatars** : Choisissez parmi les emojis ou importez votre propre image (crop intégré).
- **Cosmétiques** : 
  - Bordures animées (Rainbow, Néon, Feu, Glitch...).
  - Thèmes d'interface (Matrix, Cyber, Océan...).
  - Couleurs de pseudo.
  - Badges.
- **Packs de Mots** : Achetez de nouvelles catégories pour varier les parties.
- **Roue & Cadeaux** : Récupérez des pièces gratuites chaque jour.

##  Sauvegarde
- Vos données (Niveau, Inventaire, Amis, Historique, Battle Pass) sont sauvegardées automatiquement.
- Possibilité d'exporter/importer votre sauvegarde via les Paramètres.

## Contrôles

*   **Entrée** : Valider un mot / Envoyer un message.
*   **Maj (Shift)** : Contester une réponse (Configurable).
*   **Espace** : Passer au tour suivant (Mode Vocal).

*Développé avec Python & Pygame.*
>>>>>>> cde582d (Sauvegarde locale avant pull)
