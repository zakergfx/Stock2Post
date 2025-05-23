import { useContext, useEffect, useState } from 'react'
import "../styles/upload.scss"
import * as Api from "../utils/Api.js"
import NumericInput from '../components/NumericInput.js'
import Toggle from "../components/Toggle.js"
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import RichTextEditor from '../components/RichTextEditor.js'

function UploadPage() {

    const [makes, setMakes] = useState()
    const [selectedMake, setSelectedMake] = useState()
    const [models, setModels] = useState()
    const [selectedModel, setSelectedModel] = useState(0)
    const [selectedGarniture, setSelectedGarniture] = useState(0)
    const [km, setKm] = useState()
    const [kw, setKw] = useState()
    const [ch, setCh] = useState()
    const [images, setImages] = useState([]);

    const colors = [
        { "name": "Argent", "code": "#C0C0C0" },
        { "name": "Beige", "code": "#FFD95A" },
        { "name": "Blanc", "code": "#FFFFFF" },
        { "name": "Bleu", "code": "#0000FF" },
        { "name": "Bronze", "code": "#CD7F32" },
        { "name": "Brun", "code": "#8B4513" },
        { "name": "Gris", "code": "#808080" },
        { "name": "Jaune", "code": "#FFFF00" },
        { "name": "Mauve", "code": "#8E44AD" },
        { "name": "Noir", "code": "#000000" },
        { "name": "Or", "code": "#FFD700" },
        { "name": "Orange", "code": "#FFA500" },
        { "name": "Rouge", "code": "#FF0000" },
        { "name": "Vert", "code": "#008000" }
    ]

    const interiorColors = [
        { "name": "Beige", "code": "#FFD95A" },
        { "name": "Blanc", "code": "#FFFFFF" },
        { "name": "Bleu", "code": "#0000FF" },
        { "name": "Brun", "code": "#8B4513" },
        { "name": "Gris", "code": "#808080" },
        { "name": "Jaune", "code": "#FFFF00" },
        { "name": "Noir", "code": "#000000" },
        { "name": "Orange", "code": "#FFA500" },
        { "name": "Rouge", "code": "#FF0000" },
        { "name": "Vert", "code": "#008000" },
        { "name": "Autres", "code": "#FFFFFF" }

    ]

    const months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet",
        "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

    const years = ["2025", "2026", "2027", "2028", "2029", "2030"]

    const garnitures = ["Alcantara", "Cuir", "Cuir partiel", "Tissu", "Velours", "Autres"]

    const chassis = ["Berline", "Break", "Cabriolet", "Citadine", "Coupé", "Monospace",
        "SUV/4x4/Pick-Up", "Utilitaire", "Autres"]

    const airbags = ["Airbag arrière", "Airbag avant", "Airbag conducteur",
        "Airbag passager", "Airbag latéraux"]

    const helps = ["360° caméra", "Caméra d'aide au stationnement",
        "Capteurs d'aide au stationnement arrière", "Capteurs d'aide au stationnement avant",
        "Système d'aide au stationnement automatique"]

    const otherEquipments = ["Attache remorque", "Auvent", "Certificat de batterie",
        "Charge bidirectionnelle", "Compatible E-10", "Conduite à droite",
        "Coupe vent (pour cabriolet)", "Détecteur", "Equipement handicapé",
        "Fonctionne au biodiesel", "Frein de stationnement électronique",
        "Jantes acier", "Jantes alliage", "Kit de dépannage", "Kit fumeur",
        "Pack Sport", "Pack hiver", "Pneus neige", "Pneus tout temps saisons",
        "Pneus été", "Pompe à chaleur", "Porte-bagages", "Pot catalytique",
        "Prolongeur d'autonomie", "Roue de secours", "Roue de urgence",
        "Réglage éléctrique du siège arrière",
        "Rétroviseur intérieur anti-éblouissement automatique", "Siège arrière chauffant",
        "Suspensions sport", "Système de nettoyage des phares", "Séparateur pour coffre",
        "Trappe à ski", "Tuning", "Vitres teintées", "Eclairage d'ambiance"]

    const clims = ["Climatisation", "Climatisation automatique",
        "Climatisation automatique, 3 zones", "Climatisation automatique, 4 zones",
        "Climatisation automatique, bi-zone"]

    const comforts = ["Accoudoir", "Affichage tête haute", "Chauffage auxilaire",
        "Direction assistée", "Détecteur de lumière", "Détecteur de pluie",
        "Hayon arrière éléctrique", "Palettes de changement de vitesses",
        "Pare-brise chauffant", "Porte coulissante", "Porte coulissante droite",
        "Porte coulissante gauche", "Rétroviseurs latéreux électriques",
        "Start/Stop automatique", "Suspensions pneumatique", "Toit ouvrant",
        "Toit panoramique", "Vitres éléctriques", "Volant chauffant", "Volant en cuir"]

    const entertainments = ["Android Auto", "Apple CarPlay",
        "Chargeur Smartphone à induction", "Commande vocale", "Ecran tactile", "Fonction TV",
        "Hotspot Wi-Fi", "Radio numérique", "Soundsystem", "Streaming audio intégré",
        "USB", "Ecran multifonction entièrement numérique"]

    const medias = ["Bluetooth", "CD", "Dispositifs mains libres", "MP3",
        "Ordinateur de bord", "Radio", "Système de navigation", "Volant multifonctions"]

    const lights = ["Détecteur de lumière", "Feux anti-brouillard",
        "Feux de route non éblouissants", "LED phare de jour", "Phares Full LED",
        "Phares au LED", "Phares au Xénon", "Phares bi-xénon", "Phares de jour",
        "Phares directionnels", "Phares laser"]

    const ccs = ["Régulateur de distance", "Régulateur de vitesse"]

    const seats = ["Siège passager repliable", "Siège à réglage lombaire",
        "Sièges arrières 1/3 - 2/3", "Sièges chauffants", "Sièges massants",
        "Sièges sport", "Siège ventilés", "Sièges électriques"]

    const assists = ["Alerte de franchissement involontaire de lignes",
        "Assistant au freinage d'urgence", "Assistant de démarrage en côte",
        "Assistant de vision nocturne", "Assistant de feux de route",
        "Avertisseur d'angle mort", "Détection de panneaux routiers",
        "Limiteur de vitesse", "Système d'avertissement de distance"]

    const securities = ["ABS", "Alarme", "Anti-démarrage", "Anti-patinage", "ESP",
        "Isofix", "Système d'appel d'urgence", "Système de contrôle de la pression pneus",
        "Système de détection de la somnolence"]

    const locks = ["Verrouillage centralisé", "Verrouillage centralisé avec télécommande",
        "Verrouillage centralisé sans clé"]

    const fuels = ["Essence", "Diesel", "LPG", "CNG", "Electrique/Essence",
        "Electrique/Diesel", "Ethanol", "Electrique", "Hydrogène", "Autres"]

    async function getAllMakes() {
        const data = await Api.fetchGet("/api/makes", false)
        setMakes(data.detail)
    }

    async function getModels(make) {
        const data = await Api.fetchGet("/api/models?make=" + make, false)
        setModels(data.detail)
    }

    function handleMakeChange(e) {
        setSelectedMake(e.target.value)
        getModels(e.target.value)
    }

    function handleModelChange(e) {
        setSelectedModel(e.target.value)
    }

    function handleGarnitureChange(e) {
        setSelectedGarniture(e.currentTarget.value)
    }

    function handleKmchange(e) {
        const digits = e.target.value.replace(/\D/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ".");
        setKm(digits)
    }

    function handleKwChange(e) {
        const digits = e.target.value.replace(/\D/g, "")
        setKw(digits)
        setCh(Math.round(digits * 1.35962))
    }

    function handleChChange(e) {
        const digits = e.target.value.replace(/\D/g, "")
        setCh(digits)
        setKw(Math.round(digits / 1.35962))
    }

    function handleImageSelect(e) {
        const files = Array.from(e.target.files);

        const mapped = files.map(file => ({
            file,
            preview: URL.createObjectURL(file),
            id: crypto.randomUUID(), // identifiant unique
        }));

        setImages(prev => [...prev, ...mapped]);
    };

    function onDragEnd(result) {
        if (!result.destination) return;

        const reordered = Array.from(images);
        const [removed] = reordered.splice(result.source.index, 1);
        reordered.splice(result.destination.index, 0, removed);

        setImages(reordered);
    };

    function removeImage(id) {
        setImages(images.filter(img => img.id !== id));
    };

    useEffect(getAllMakes, [])

    //[{"id":2,"as_id":0,"name":"Audi"},{"id":4,"as_id":1,"name":"BMW"}]

    return (<div className="UploadPage">
        <div className="Content">

            <div className="Section">
                <h2>Données du véhicule</h2>
                <label>Marque*</label>
                <select value={selectedMake} onChange={handleMakeChange}>
                    <option>Veuillez choisir</option>
                    {makes && makes.map((make, index) => <option key={index}>{make.name}</option>)}
                </select>
                <label>Modèle*</label>
                <select value={selectedModel} onChange={handleModelChange}>
                    <option>Veuillez choisir</option>
                    {models && models.map((model, index) => <option key={index}>{model.name}</option>)}
                </select>
                <label>Variante du modèle</label>
                <input placeholder="par ex.: Avant 1.4 TSI S-Tronic" type="input" maxLength={50}></input>
            </div>

            <div className="Section">
                <h2>Caractéristiques</h2>
                <label>Type de châssis*</label>
                <select>
                    <option>Veuillez choisir</option>
                    {chassis.map((chassi, index) => <option key={index}>{chassi}</option>)}
                </select>
                <label>Sièges</label>
                <NumericInput />
                <label>Portes</label>
                <NumericInput />
                <label>Couleur</label>
                <div className="Colors">
                    {colors.map((color, index) => <div key={index} className="ColorSection">
                        <span className="Color" style={{ backgroundColor: color.code }}></span>
                        <label>{color.name}</label>
                    </div>)}
                </div>
                <label>Peinture</label>
                <div className="ToggleSection">
                    <input type="checkbox"></input>
                    <label>Métalisé</label>
                </div>
                <label>Garniture</label>
                <div className="GarnitureSection">
                    {garnitures.map((garniture, index) => <div key={index} className="Garniture">
                        <input type="radio" name="garniture" value={garniture} onClick={handleGarnitureChange} />
                        <label>{garniture}</label>
                    </div>)}
                </div>
                <label>Couleur intérieure</label>
                <div className="Colors">
                    {interiorColors.map((color, index) => <div key={index} className="ColorSection">
                        <span className="Color" style={{ backgroundColor: color.code }}></span>
                        <label>{color.name}</label>
                    </div>)}
                </div>
                <h2>Condition</h2>
                <label>Type de véhicule*</label>
                <select>
                    <option>Veuillez choisir</option>
                    <option>Occasion</option>
                    <option>Ancêtre</option>
                </select>
                <label>Kilométrage*</label>
                <input type="text" maxLength={7} inputMode='numeric' value={km} onChange={handleKmchange}></input>
                <label>Nombre de propriétaires précédents</label>
                <NumericInput />
                <div className="ToggleSection">
                    <label>Carnet d'entretien complet</label>
                    <input type="checkbox"></input>
                </div>
                <div className="ToggleSection">
                    <label>Véhicule non fumeur</label>
                    <input type="checkbox"></input>
                </div>
                <label>Prochaine révision</label>
                <div className="Selects">
                    <select>
                        <option>Mois</option>
                        {months.map((month, index) => <option key={index}>{month}</option>)}
                    </select>
                    <select>
                        <option>Année</option>
                        {years.map((year, index) => <option key={index}>{year}</option>)}
                    </select>
                </div>
                <label>Dernier entretien</label>
                <div className="Selects">
                    <select>
                        <option>Mois</option>
                        {months.map((month, index) => <option key={index}>{month}</option>)}
                    </select>
                    <select>
                        <option>Année</option>
                        {years.map((year, index) => <option key={index}>{year}</option>)}
                    </select>
                </div>
                <label>Date changement de courroie de distribution</label>
                <div className="Selects">
                    <select>
                        <option>Mois</option>
                        {months.map((month, index) => <option key={index}>{month}</option>)}
                    </select>
                    <select>
                        <option>Année</option>
                        {years.map((year, index) => <option key={index}>{year}</option>)}
                    </select>
                </div>
                <div className="ToggleSection">
                    <input type="checkbox"></input>
                    <label>Véhicule accidenté</label>
                </div>
                <h2>Equipement</h2>
                <label>Airbag</label>
                <div className="Equipments">
                    {airbags.map((option, index) => <div key={index} className="ToggleSection">
                        <input type="checkbox"></input>
                        <label>{option}</label>
                    </div>)}
                </div>
                <label>Assistant au stationnement</label>
                <div className="Equipments">
                    {helps.map((option, index) => <div key={index} className="ToggleSection">
                        <input type="checkbox"></input>
                        <label>{option}</label>
                    </div>)}
                </div>
                <label>Autres</label>
                <div className="Equipments">
                    {otherEquipments.map((option, index) => <div key={index} className="ToggleSection">
                        <input type="checkbox"></input>
                        <label>{option}</label>
                    </div>)}
                </div>
                <label>Climatisation</label>
                <div className="Equipments">
                    {clims.map((option, index) => <div key={index} className="ToggleSection">
                        <input type="checkbox"></input>
                        <label>{option}</label>
                    </div>)}
                </div>
                <label>Confort</label>
                <div className="Equipments">
                    {comforts.map((option, index) => <div key={index} className="ToggleSection">
                        <input type="checkbox"></input>
                        <label>{option}</label>
                    </div>)}
                </div>
                <label>Divertissement</label>
                <div className="Equipments">
                    {entertainments.map((option, index) => <div key={index} className="ToggleSection">
                        <input type="checkbox"></input>
                        <label>{option}</label>
                    </div>)}
                </div>
                <label>Divertissement / Médias</label>
                <div className="Equipments">
                    {medias.map((option, index) => <div key={index} className="ToggleSection">
                        <input type="checkbox"></input>
                        <label>{option}</label>
                    </div>)}
                </div>
                <label>Lumière</label>
                <div className="Equipments">
                    {lights.map((option, index) => <div key={index} className="ToggleSection">
                        <input type="checkbox"></input>
                        <label>{option}</label>
                    </div>)}
                </div>
                <label>Régulateur de vitesse</label>
                <div className="Equipments">
                    {ccs.map((option, index) => <div key={index} className="ToggleSection">
                        <input type="checkbox"></input>
                        <label>{option}</label>
                    </div>)}
                </div>
                <label>Sièges</label>
                <div className="Equipments">
                    {seats.map((option, index) => <div key={index} className="ToggleSection">
                        <input type="checkbox"></input>
                        <label>{option}</label>
                    </div>)}
                </div>
                <label>Systèmes d'assistance</label>
                <div className="Equipments">
                    {assists.map((option, index) => <div key={index} className="ToggleSection">
                        <input type="checkbox"></input>
                        <label>{option}</label>
                    </div>)}
                </div>
                <label>Sécurité</label>
                <div className="Equipments">
                    {securities.map((option, index) => <div key={index} className="ToggleSection">
                        <input type="checkbox"></input>
                        <label>{option}</label>
                    </div>)}
                </div>
                <label>Verrouillage centralisé</label>
                <div className="Equipments">
                    {locks.map((option, index) => <div key={index} className="ToggleSection">
                        <input type="checkbox"></input>
                        <label>{option}</label>
                    </div>)}
                </div>
                <h2>Moteur</h2>
                <label>Transmission</label>
                <select>
                    <option>Veuillez choisir</option>
                    <option>4x4</option>
                    <option>Avant</option>
                    <option>Arrière</option>
                </select>
                <label>Type de boîte</label>
                <select>
                    <option>Veuillez choisir</option>
                    <option>Boîte automatique</option>
                    <option>Boîte manuelle</option>
                    <option>Semi-automatique</option>
                </select>
                <label>Puissance*</label>
                <input value={kw} inputMode="numeric" onChange={handleKwChange}></input>
                <input value={ch} inputMode="numeric" onChange={handleChChange}></input>
                <label>Nombre de vitesses</label>
                <NumericInput />
                <label>Nombre de cylindres</label>
                <NumericInput />
                <label>Cylindrée</label>
                <input placeholder="par ex 1999 cm3" inputMode="numeric"></input>
                <label>Poids à vide</label>
                <input placeholder="par ex 1550 kg" inputMode="numeric"></input>
                <h2>Environnement</h2>
                <label>Type de carburant</label>
                <select>
                    <option>Veuillez choisir</option>
                    {fuels.map((fuel, index) => <option key={index}>{fuel}</option>)}
                </select>
                <div className="Co2">
                    <input type="radio" name="co2" value="NEDC" />
                    <label>NEDC</label>
                </div>
                <div className="Co2">
                    <input type="radio" name="co2" value="WLTP" />

                    <label>WLTP</label>
                </div>
            <h2>Photos</h2>
            <p>Un maximum de 50 images peuvent être téléchargées. Veuillez télécharger uniquement des images au format JPEG ou PNG.</p>
            <input type="file" multiple accept="image/*" onChange={handleImageSelect} />

            <DragDropContext onDragEnd={onDragEnd}>
                <Droppable droppableId="images" direction="horizontal">
                    {(provided) => (
                        <div className="ImgContainer" {...provided.droppableProps} ref={provided.innerRef}>
                            {images.map((img, index) => (
                                <Draggable key={img.id} draggableId={img.id} index={index}>
                                    {(provided) => (
                                        <div
                                            ref={provided.innerRef}
                                            {...provided.draggableProps}
                                            {...provided.dragHandleProps}
                                        >
                                            <div className="ImgSubContainer">
                                                <img src={img.preview} alt="preview" width={200} />
                                                <button onClick={() => removeImage(img.id)}>X</button>
                                            </div>

                                        </div>
                                    )}
                                </Draggable>
                            ))}
                            {provided.placeholder}
                        </div>
                    )}
                </Droppable>
            </DragDropContext>

            <h2>Description du véhicule</h2>
            <RichTextEditor/>
                
                <h2>Prix public taxes incluses</h2>
                <label>Prix tout compris*</label>
                <input placeholder="Introduire une valeur" inputMode='numeric'></input>
                <div className="ToggleSection">
                    <input type="checkbox"></input>
                    <label>Prix à débattre</label>
                </div>
                <div className="ToggleSection">
                    <input type="checkbox"></input>
                    <label>TVA déductible</label>
                </div>
            </div>

        </div>
    </div>)

}

export default UploadPage