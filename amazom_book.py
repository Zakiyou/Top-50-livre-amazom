import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger vos données (remplacez cela par vos propres données)
data = pd.read_csv("top_50_book_amazom.csv")

# Nombre total de différents livres vendus
nb_total_unique = data['Name'].nunique()
note_moy_livre = data['User Rating'].mean()

# Top 5 des livres avec le plus grand nombre de critiques
top_5_critiques = data.groupby('Name')['Reviews'].sum().sort_values(ascending=False).head(5)
top_5_critiques = top_5_critiques.rename_axis('Livre').reset_index(name='Critiques')
# Top 5 livres avec le plus grand nombre d'apparitions
nb_apparition_livre = data['Name'].value_counts().sort_values(ascending=False).head(5)
nb_apparition_livre = nb_apparition_livre.rename_axis('Livre').reset_index(name='Apparition')
# livre avec le prix le plus élevé 
livre_prix_eleve=data.groupby('Name')['Price'].sum().sort_values(ascending=False).head(1)
# Calculer la répartition des genres
repartition_genre = data.groupby('Name').first()['Genre'].value_counts()
# Calcul de la corrélation
correlation = data['User Rating'].corr(data['Price'])
#Evolution des critiques totales en fonction d'année
nb_critique_par_année=data.groupby('Year')['Reviews'].sum()
nb_critique_par_année =nb_critique_par_année.rename_axis('Année').reset_index(name='nombre_critique_total')
#Evolution des notes moyennes en fonction d'année
nb_note_par_année=data.groupby('Year')['User Rating'].mean()
nb_note_par_année =nb_note_par_année.rename_axis('Année').reset_index(name='nombre_note_moyenne')
# Répartition de genre en fonction de nombre de critique
repartition_genre_critique = data.groupby('Genre')['Reviews'].sum()
repartition_genre_critique = repartition_genre_critique.rename_axis('Genre').reset_index(name='Reviews')

# Titre du tableau de bord
st.title('Analyse de la dataset contenant les 50 meilleurs livres d\'Amazon chaque année entre 2009 et 2019')

# Panneau d'administration à gauche avec onglets
with st.sidebar:
    st.markdown('## Panneau d\'administration')
    onglet_selectionne = st.radio('Sélectionnez une visualisation', ['Description de la dataset','Nombre total de livres', 'Note moyenne des livres', 'Top 5 des livres avec le plus grand critiques','top 5 de livre avec le plus apparitions','livre avec le prix le plus  elevé','Correlation entre note et prix de livre','Repartition genre de livre','Évolution des critiques par année','Évolution du la moyenne de note au fil des années','Répartition des genres par nombre de critiques'])

if onglet_selectionne == 'Description de la dataset':
    st.write('## 1-Description de la dataset')
    st.markdown("""
Cet ensemble de données Excel compile des informations sur les 50 livres les plus vendus sur la plateforme Amazon, chaque année entre 2009 et 2019. Les variables incluses dans cet ensemble offrent un aperçu complet des caractéristiques de chaque livre, permettant une analyse approfondie de leur popularité et de leurs attributs.
""")
    st.markdown("""
1. **Nom (Name):** Cette variable représente le titre de chaque livre. Chaque entrée est le nom unique attribué à un livre particulier.

2. **Auteur (Author):** La variable "Auteur" indique le nom de l'auteur du livre. Elle permet d'identifier les créateurs derrière chaque œuvre.

3. **Note des utilisateurs (User Rating):** Il s'agit de la note moyenne attribuée par les utilisateurs d'Amazon à chaque livre. Cette variable offre un aperçu de la satisfaction globale des lecteurs.

4. **Critiques (Reviews):** La variable "Critiques" représente le nombre total de critiques reçues par chaque livre sur la plateforme Amazon. Cela reflète l'engagement et l'intérêt des lecteurs.

5. **Prix (Price):** Indiquant le coût en dollars américains, la variable "Prix" renseigne sur le prix du livre. Cette information peut être utile pour explorer les relations entre le coût et la popularité.

6. **Année (Year):** L'année de publication du livre est enregistrée dans cette variable. Elle permet de suivre l'évolution des ventes au fil des années.

7. **Genre (Genre):** Cette variable catégorise chaque livre en fonction de son genre. Elle offre des insights sur les préférences des lecteurs et les tendances littéraires.
""")

if onglet_selectionne == 'Nombre total de livres':
    st.write('## 2-Nombre total de différents livres dans la dataset')
    
    plt.figure(figsize=(3, 3))
    ax = plt.gca()
    ax.axis('off')
    ax.table(cellText=[[nb_total_unique]], colLabels=['Nombre total de différents livres dans la dataset'], cellLoc='center', loc='center')
    st.pyplot(plt)
    st.write("351 livres différents se retrouvent dans la dataset. Cela représente la diversité des titres proposés sur Amazon au cours de la période.")


elif onglet_selectionne == 'Note moyenne des livres':
    st.write('## 3-Note moyenne des livres')
    plt.figure(figsize=(3, 3))
    ax = plt.gca()
    ax.axis('off')
    ax.table(cellText=[[note_moy_livre]], colLabels=['Note moyenne des livres'], cellLoc='center', loc='center')
    st.pyplot(plt)
    st.write("La note moyenne des livres est de ",note_moy_livre,". Cela suggère une qualité globalement élevée des livres sélectionnés.")

elif onglet_selectionne == 'Top 5 des livres avec le plus grand critiques':
    st.subheader('4- Top 5 des livres avec le plus grand nombre de critiques')
    palette = sns.color_palette("husl", len(top_5_critiques['Critiques']))
    plt.figure(figsize=(10, 6))
    bars = plt.barh(top_5_critiques['Livre'], top_5_critiques['Critiques'], color=palette)
    plt.legend(bars, top_5_critiques['Critiques'], title='Critiques', loc='upper right')

    plt.xlabel('Nombre de critiques total par livre')
    plt.title('Top 5 des livres avec le plus grand nombre de critiques')
    plt.grid(axis='x')
    st.pyplot(plt)
    st.write("""
    Les livres suivants ont reçu le plus grand nombre de critiques sur Amazon :
    1. *The Fault in Our Stars* avec 201928 critiques.
    2. *Oh, the Places You'll Go!* avec 174672 critiques.
    3. *Gone Girl* avec 171813 critiques.
    4. *The Girl on the Train* avec 158892 critiques.
    5. *Unbroken: A World War II Story of Survival, Resilience, and Redemption* avec 148365 critiques.
     """)
elif onglet_selectionne =='top 5 de livre avec le plus apparitions':
    st.subheader("5-Top 5 livres avec le plus grand nombre d'apparitions :")
    plt.figure(figsize=(10, 6))
    palette = sns.color_palette("pastel")[:len(nb_apparition_livre)]
    bars = plt.bar(nb_apparition_livre['Livre'], nb_apparition_livre['Apparition'], color=palette)
    plt.title('Top 5 livres avec le plus grand nombre d\'apparitions')
    plt.xlabel('Livre')
    plt.ylabel('Apparition')

    plt.xticks(rotation=90, ha="right")
    for bar, apparition in zip(bars, nb_apparition_livre['Apparition']):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, str(apparition), ha='center', va='bottom', rotation=0)
    st.pyplot(plt)
elif onglet_selectionne =='livre avec le prix le plus  elevé':
    st.subheader("6-Livre avec le prix total le plus élevé :")
    st.write("Le graphique ci-dessous présente le livre qui a accumulé le prix total le plus élevé sur la période de 2009 à 2019.")
    plt.figure(figsize=(8, 6))
    palette = sns.color_palette("pastel")
    bar = plt.bar(livre_prix_eleve.index, livre_prix_eleve.values, color=palette)
    plt.title('Livre avec le prix total le plus élevé')
    plt.xlabel('Livre')
    plt.ylabel('Prix total')

    for b in bar:
        plt.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.5, str(b.get_height()), ha='center', va='bottom')

    st.pyplot(plt)
elif onglet_selectionne == 'Correlation entre note et prix de livre':
    st.subheader("7-Corrélation entre la note et le prix des livres :")
    st.write("Le coefficient de corrélation mesure la relation linéaire entre la note moyenne des utilisateurs et le prix des livres. "
             "Il varie de -1 à 1, où -1 indique une corrélation négative parfaite, 1 une corrélation positive parfaite et 0 aucune corrélation.")

    plt.figure(figsize=(6, 4))
    ax = plt.gca()
    ax.axis('off')
    ax.table(cellText=[[correlation]], colLabels=['Corrélation'], cellLoc='center', loc='center')
    st.pyplot(plt)
elif onglet_selectionne == 'Repartition genre de livre':
    st.subheader("8-Répartition des genres des livres :")
    st.write("Le graphique circulaire ci-dessous illustre la répartition des genres parmi les livres de  l'ensemble de données. "
             "Chaque portion représente la proportion d'un genre par rapport au total des livres.")

    plt.figure(figsize=(8, 8))
    plt.pie(repartition_genre, labels=repartition_genre.index, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightgreen'])

    plt.title('Répartition des genres des livres')
    plt.legend(repartition_genre.index, title='Genre', loc='upper right')
    st.pyplot(plt)

elif onglet_selectionne == 'Évolution des critiques par année':
    st.subheader('9- Évolution du nombre total de critiques au fil des années')
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.plot(nb_critique_par_année['Année'], nb_critique_par_année['nombre_critique_total'], marker='o', linestyle='-', color='#27AC75')
    plt.title('Évolution du nombre total de critiques au fil des années')
    plt.xlabel('Année')
    plt.ylabel('Nombre total de critiques')
    for i, txt in enumerate(nb_critique_par_année['nombre_critique_total']):
        ax.text(nb_critique_par_année['Année'][i], txt, f"{txt:.2f}", ha='left', va='bottom', fontsize=8, color='#7F41E2')
    plt.grid(True)
    plt.xticks(nb_critique_par_année['Année'])
    st.pyplot(fig)

elif onglet_selectionne == 'Évolution du la moyenne de note au fil des années':
    st.subheader('10-Évolution du le moyenne de note au fil des années')
    plt.figure(figsize=(10, 10))
    plt.plot(nb_note_par_année['Année'], nb_note_par_année['nombre_note_moyenne'], marker='o', linestyle='-', color='#E76A30')
    plt.title('Évolution de la moyenne de note au fil des années')
    plt.xlabel('Année')
    plt.ylabel('Moyenne de note')
    for i, txt in enumerate(nb_note_par_année['nombre_note_moyenne']):
        plt.text(nb_note_par_année['Année'][i], txt, f"{txt:.2f}", ha='left', va='bottom', fontsize=8, color='#320875')
    plt.grid(True)
    plt.xticks(nb_note_par_année['Année'])
    st.pyplot(plt)

elif onglet_selectionne == 'Répartition des genres par nombre de critiques':
    st.subheader('11-Répartition des genres par nombre de critiques')
    plt.figure(figsize=(8, 8))
    plt.pie(repartition_genre_critique['Reviews'], labels=repartition_genre_critique['Genre'], autopct='%1.1f%%', startangle=90, pctdistance=0.85, wedgeprops=dict(width=0.3), colors=['skyblue', 'lightpink'])
    centre_cercle = plt.Circle((0, 0), 0.60, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_cercle)
    plt.legend(repartition_genre_critique['Genre'], title='Catégories', loc='upper right')
    plt.title('Répartition des genres par nombre de critiques')

    st.pyplot(plt)
    
st.balloons()
st.markdown("Réalisé par **bababodi zakiyou** - Analyste programmeur et Data scientist")