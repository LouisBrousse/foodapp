// Faire une application Express qui affiche des données sur les aliments à partir de la BD Ciqual.

//     la page d’accueil est un formulaire constitué d’un seul champ de texte où on peut taper des mots-clés, puis cliquer sur un bouton ‘Valider’
//     la page suivante affiche la liste des aliments dont les noms contiennent un des mots clés saisis
//     un clic sur un des aliments de la liste affiche une page donnant les valeurs nutritionnelles de l’aliments pour quelques nutriments

import express from 'express';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();
const app = express();

app.set('view engine', 'ejs')

app.use(express.urlencoded({ extended: true }));

app.get ("/", function (req, res){
    res.render('acceuil')
})

app.post("/getkw", async (req, res) => {
    //getting the keyword
    const keyword = req.body.keyword;
    //looking in table food if keyword is in it

    const foodkwlist = await prisma.food.findMany({
        where: {
            name :{
                contains: keyword.toLowerCase()
                
            },
        },
    }) 
   
    res.render('foodlist', {foodkwlist})
      
});

app.get("/getid/:id", async (req, res) => {         // en fesant "/___/:___" il va attendre n'importe quelle entrée que la page foodlist renverra avec sont href
    const foodid= req.params.id //donc je recupère le numerod'id
    const nutlistfood = await prisma.nutdata.findMany ({
        where: {
            food_id :{
                equals: foodid
            },
            value: {
                not: {
                    equals: '-',
                },
            },
        },
    })
    
    console.log("list des nuts de la food", nutlistfood)
    
    const nutlist = await prisma.nutrient.findMany()
    console.log("list des nuts", nutlist)
    
    

    const nutrientDict = {};
    nutlist.forEach((entry) => {
        nutrientDict[entry.id] = entry.name;
    });

    const nutrilist = nutlistfood.map((entry) => ({
        [nutrientDict[entry.nutrient_id]]: entry.value,
    }));
    
    res.render('nutvalues', { nutrilist })
    
    
}) 









app.listen(3000, function () {
    console.log('Server listening on port 3000');
 });
 