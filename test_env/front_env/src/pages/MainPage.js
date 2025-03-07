import { useEffect, useState, useContext } from 'react'
import "../styles/main.scss"
import FacebookLoginButton from '../components/FacebookLoginButton'
import * as Api from "../utils/Api.js"
import { AuthContext } from '../context/AuthContext.js'
import { MainContext } from '../context/MainContext.js'

import Alert from '../components/Alert.js'
import Toggle from '../components/Toggle.js'

function MainPage() {
    const { isMobile } = useContext(MainContext)

    const [enablePageManagemenent, setEnablePageManagement] = useState()

    const [enablePostNewCar, setEnablePostNewCar] = useState()
    const [enablePostNewCarStory, setEnablePostNewCarStory] = useState()

    const [enablePostSoldCar, setEnablePostSoldCar] = useState()

    const [enablePostOldCar, setEnablePostOldCar] = useState()
    const [oldCarHz, setOldCarHz] = useState()

    const [enablePostDiscount, setEnablePostDiscount] = useState()
    const [enableModifiedPost, setEnableModifiedPost] = useState()

    const [enablePostStockSummary, setEnablePostStockSummary] = useState()
    const [summaryHz, setSummaryHz] = useState()

    const [dealerInfos, setDealerInfos] = useState()

    const [testMode, setTestMode] = useState(false)



    async function testingPost(e) {
        e.preventDefault()
        console.log("Envoi de la demande de création du post")
        Alert.info("Test en cours. Celà peut prendre jusqu'à 1 minute.")
        const success = (await Api.fetchPost("/api/testing/", { "scenario": parseInt(e.target.id) })).success
        console.log(success)
        if (success) {
            Alert.success("Le post a bien été créé.")
        }
        else {
            Alert.error("Le post n'a pas pu être créé.")
        }
    }

    // récupération infos dealers
    useEffect(() => {
        async function fetchData() {
            const infos = (await Api.fetchGet(`/api/me`)).detail

            const data = (await Api.fetchGet(`/api/dealers/${infos.user}/`)).detail
            setDealerInfos(data)

            setEnablePageManagement(data.fk_settings.pageIsManaged)
            setEnablePostNewCar(data.fk_settings.createNewCarPost)
            setEnablePostNewCarStory(data.fk_settings.createNewCarStory)
            setEnablePostOldCar(data.fk_settings.createOldCarPost)
            setEnablePostSoldCar(data.fk_settings.createSoldCarPost)
            setEnablePostDiscount(data.fk_settings.createDiscountCarPost)
            setEnableModifiedPost(data.fk_settings.createModifiedPost)
            setEnablePostStockSummary(data.fk_settings.createSummaryPost)
            setOldCarHz(data.fk_settings.oldCarPostDelay)
            setSummaryHz(data.fk_settings.summaryPostDelay)

        }
        fetchData()


    }, [])

    async function handleButtonClick(e) {
        e.preventDefault()
        const settings = {
            "pageIsManaged": enablePageManagemenent,
            "createNewCarPost": enablePostNewCar,
            "createOldCarPost": enablePostOldCar,
            "createSoldCarPost": enablePostSoldCar,
            "createNewCarStory": enablePostNewCarStory,
            "createDiscountCarPost": enablePostDiscount,
            "createModifiedPost": enableModifiedPost,
            "createSummaryPost": enablePostStockSummary,
            "oldCarPostDelay": oldCarHz,
            "summaryPostDelay": summaryHz
        }

        const response = await Api.fetchPatch(`/api/dealers/${dealerInfos.name}/settings/`, settings)
        if (response.success) {
            Alert.success("Sauvegarde effectuée !")
        }
        else {
            Alert.error("Erreur lors de la sauvegarde des paramètres !")
        }

    }

    function handleOldCarHz(e) {
        const hz = parseInt(e.target.value)
        setOldCarHz(hz)
        setEnablePostOldCar(hz!==0)
    }

    function handleSummaryHz(e) {
        const hz = parseInt(e.target.value)
        setSummaryHz(hz)
        setEnablePostStockSummary(hz!==0)
    }

    return (<div className="MainPage">
        {dealerInfos && <div className="Content">

            <div className="Title">
                <h1>Page de configuration </h1>
                <div className="Testmode">
                    <span>Activer le mode Test</span>
                    <Toggle isActive={testMode} setFct={setTestMode} />
                </div>
            </div>
            <div className="Settings">
                <form className={testMode ? "Test" : "Prod"}>
                    <h2>Fonctionnalités</h2>
                    <h2>Activé</h2>
                    {testMode && !isMobile && <h2>Test</h2>}

                    <div className="Setting">
                        <b>Activer la gestion de ma page</b>
                        <span>Si cette option n'est pas activée alors aucun post ne sera publié sur votre page Facebook</span>
                    </div>

                    <Toggle isActive={enablePageManagemenent} setFct={setEnablePageManagement} />
                    {!isMobile && testMode && <span></span>}
                    {enablePageManagemenent && <>
                        <div className="Setting">
                            <b>Créer un post quand un véhicule est ajouté à votre catalogue</b>
                            <span>Quand un véhicule est ajouté à votre catalogue AutoScout, un post sera créé.</span>
                        </div>
                        <Toggle isActive={enablePostNewCar} setFct={setEnablePostNewCar} />
                        {testMode && <button id="0" onClick={testingPost}>Tester</button>}
                        {testMode && isMobile && <span />}
                        <div className="Setting">
                            <b>Publier également une Story</b>
                            <span>En plus de créer un post Facebook annonçant le nouvel arrivage, une story sera également publiée.</span>
                        </div>

                        <Toggle isActive={enablePostNewCarStory} setFct={setEnablePostNewCarStory} />
                        {testMode && <button id="6" onClick={testingPost}>Tester</button>}
                        {testMode && isMobile && <span />}

                        <div className="Setting">
                            <b>Créer un post quand un véhicule a été vendu</b>
                            <span>Quand un véhicule est retiré de votre catalogue il sera considéré comme vendu. Un post sera créé pour signaler la vente.</span>
                        </div>
                        <Toggle isActive={enablePostSoldCar} setFct={setEnablePostSoldCar} />
                        {testMode && <button id="1" onClick={testingPost}>Tester</button>}
                        {testMode && isMobile && <span />}

                        <div className="Setting">
                            <b>Créer des posts de rappel</b>
                            <span>Si un véhicule est présent depuis longtemps dans votre catalogue mais n’a toujours pas trouvé preneur, un post sera créé toutes les X semaines afin de remettre l’annonce en avant.</span>
                        </div>

                        <select value={oldCarHz} onChange={handleOldCarHz}>
                            <option value="0">Jamais</option>
                            <option value="1">1 semaine</option>
                            <option value="2">2 semaines</option>
                            <option value="3">3 semaines</option>
                            <option value="4">4 semaines</option>
                            <option value="5">5 semaines</option>
                            <option value="6">6 semaines</option>
                            <option value="7">7 semaines</option>
                            <option value="8">8 semaines</option>
                            <option value="9">9 semaines</option>
                            <option value="10">10 semaines</option>
                            <option value="11">11 semaines</option>
                            <option value="12">12 semaines</option>
                        </select>

                        {testMode && <button id="2" onClick={testingPost}>Tester</button>}
                        {testMode && isMobile && <span />}

                        <div className="Setting">
                            <b>Créer un post quand une réduction a lieu sur un véhicule</b>
                            <span>Lorsque le prix d’un véhicule est diminué, un post est réalisé pour le mettre en avant.</span>
                        </div>
                        <Toggle isActive={enablePostDiscount} setFct={setEnablePostDiscount} />
                        {testMode && <button id="3" onClick={testingPost}>Tester</button>}
                        {testMode && isMobile && <span />}


                        <div className="Setting">
                            <b>Créer un post quand une modification d’une annonce a lieu</b>
                            <span>Si la page AutoScout d’un véhicule est modifiée, un nouveau post sera créé pour signaler que la page a été changée.</span>
                        </div>
                        <Toggle isActive={enableModifiedPost} setFct={setEnableModifiedPost} />
                        {testMode && <button id="4" onClick={testingPost}>Tester</button>}
                        {testMode && isMobile && <span />}

                        <div className="Setting">
                            <b>Créer un post récapitulatif du stock</b>
                            <span>Un post récapitulatif qui reprend l’ensemble de votre stock peut être planifié toutes les X semaines.</span>
                        </div>
                        <select value={summaryHz} onChange={handleSummaryHz}>
                            <option value="0">Jamais</option>
                            <option value="1">1 semaine</option>
                            <option value="2">2 semaines</option>
                            <option value="3">3 semaines</option>
                            <option value="4">4 semaines</option>
                            <option value="5">5 semaines</option>
                            <option value="6">6 semaines</option>
                            <option value="7">7 semaines</option>
                            <option value="8">8 semaines</option>
                            <option value="9">9 semaines</option>
                            <option value="10">10 semaines</option>
                            <option value="11">11 semaines</option>
                            <option value="12">12 semaines</option>
                        </select>
                        {testMode && <button id="5" onClick={testingPost}>Tester</button>}
                        {testMode && isMobile && <span />}

                    </>}
                    <input onClick={handleButtonClick} type="Submit" className="Submit Primary" value={!isMobile ? "Sauvegarder les changements" : "Sauvegarder"}></input>

                </form>
            </div>

        </div>}
    </div>)
}

export default MainPage