import { useEffect, useState, useContext } from 'react'
import "../styles/main.scss"
import FacebookLoginButton from '../components/FacebookLoginButton'
import * as Api from "../utils/Api.js"
import { AuthContext } from '../context/AuthContext.js'
import { MainContext } from '../context/MainContext.js'

import Alert from '../components/Alert.js'
import Toggle from '../components/Toggle.js'
import ToolTip from '../components/ToolTip.js'

function MainPage() {
    const { isMobile } = useContext(MainContext)

    const [FBpageIsPaused, setFBpageIsPaused] = useState()
    const [FBcreateNewCarPost, setFBcreateNewCarPost] = useState()
    const [FBcreateNewCarStory, setFBcreateNewCarStory] = useState()
    const [FBcreateSoldCarPost, setFBcreateSoldCarPost] = useState()
    const [FBcreateOldCarPost, setFBcreateOldCarPost] = useState()
    const [FBcreateDiscountCarPost, setFBcreateDiscountCarPost] = useState()
    const [FBoldCarPostDelay, setFBoldCarPostDelay] = useState()
    const [FBlastNewCarPostEnabled, setFBlastNewCarPostEnabled] = useState()

    const [IGpageIsPaused, setIGpageIsPaused] = useState()
    const [IGcreateNewCarPost, setIGcreateNewCarPost] = useState()
    const [IGcreateNewCarStory, setIGcreateNewCarStory] = useState()
    const [IGcreateSoldCarPost, setIGcreateSoldCarPost] = useState()
    const [IGcreateOldCarPost, setIGcreateOldCarPost] = useState()
    const [IGcreateDiscountCarPost, setIGcreateDiscountCarPost] = useState()
    const [IGoldCarPostDelay, setIGoldCarPostDelay] = useState()
    const [IGlastNewCarPostEnabled, setIGlastNewCarPostEnabled] = useState()


    const [dealerInfos, setDealerInfos] = useState()
    const [testMode, setTestMode] = useState(false)

    async function getRequestStatus() {
        const response = await Api.fetchGet("/api/requeststatus")
        return response.detail.status
    }


    function promise() {

        return new Promise(async (resolve, reject) => {

            function sleep(ms) {
                return new Promise(resolve => setTimeout(resolve, ms));
            }

            while (true) {
                const status = await getRequestStatus()
                if (status === "success") {

                    resolve("Success !")
                    return
                }

                else if (status === "error") {
                    reject(("Error !"))
                    return
                }
                console.log("status: " + status)
                await sleep(5000)
            }
        })
    }

    async function testingPost(e) {
        e.preventDefault()
        const requestInProgress = await getRequestStatus()
        if (requestInProgress !== "pending") {

            console.log("Envoi de la demande de création du post")
            const success = (await Api.fetchPost("/api/testing/", { "scenario": parseInt(e.target.id) })).success
            if (success) {
                Alert.promise(promise)
            }
            else {
                Alert.error("La demande de création de post n'a pas pu aboutit")
            }
        }
        else {
            Alert.error("Vous avez déjà une requête en attente")
        }

    }

    // récupération infos dealers
    useEffect(() => {
        async function fetchData() {
            const infos = (await Api.fetchGet(`/api/me`)).detail

            const data = (await Api.fetchGet(`/api/dealers/${infos.user}/`)).detail
            setDealerInfos(data)

            console.log(data.fk_settings)

            setFBpageIsPaused(data.fk_settings.FBpageIsPaused)
            setFBcreateNewCarPost(data.fk_settings.FBcreateNewCarPost)
            setFBcreateNewCarStory(data.fk_settings.FBcreateNewCarStory)
            setFBcreateSoldCarPost(data.fk_settings.FBcreateSoldCarPost)
            setFBcreateOldCarPost(data.fk_settings.FBcreateOldCarPost)
            setFBcreateDiscountCarPost(data.fk_settings.FBcreateDiscountCarPost)
            setFBoldCarPostDelay(data.fk_settings.FBoldCarPostDelay)
            setFBlastNewCarPostEnabled(data.fk_settings.FBlastNewCarPostEnabled)

            setIGpageIsPaused(data.fk_settings.IGpageIsPaused)
            setIGcreateNewCarPost(data.fk_settings.IGcreateNewCarPost)
            setIGcreateNewCarStory(data.fk_settings.IGcreateNewCarStory)
            setIGcreateSoldCarPost(data.fk_settings.IGcreateSoldCarPost)
            setIGcreateOldCarPost(data.fk_settings.IGcreateOldCarPost)
            setIGcreateDiscountCarPost(data.fk_settings.IGcreateDiscountCarPost)
            setIGoldCarPostDelay(data.fk_settings.IGoldCarPostDelay)
            setIGlastNewCarPostEnabled(data.fk_settings.IGlastNewCarPostEnabled)

        }
        fetchData()

    }, [])

    async function handleButtonClick(e) {
        e.preventDefault()
        const settings = {

            "FBpageIsPaused": FBpageIsPaused,
            "FBcreateNewCarPost": FBcreateNewCarPost,
            "FBcreateNewCarStory": FBcreateNewCarStory,
            "FBcreateSoldCarPost": FBcreateSoldCarPost,
            "FBcreateOldCarPost": FBcreateOldCarPost,
            "FBcreateDiscountCarPost": FBcreateDiscountCarPost,
            "FBoldCarPostDelay": FBoldCarPostDelay,
            "FBlastNewCarPostEnabled": FBlastNewCarPostEnabled,
            "IGpageIsPaused": IGpageIsPaused,
            "IGcreateNewCarPost": IGcreateNewCarPost,
            "IGcreateNewCarStory": IGcreateNewCarStory,
            "IGcreateSoldCarPost": IGcreateSoldCarPost,
            "IGcreateOldCarPost": IGcreateOldCarPost,
            "IGcreateDiscountCarPost": IGcreateDiscountCarPost,
            "IGoldCarPostDelay": IGoldCarPostDelay,
            "IGlastNewCarPostEnabled": IGlastNewCarPostEnabled
        }


        const response = await Api.fetchPatch(`/api/dealers/${dealerInfos.name}/settings/`, settings)
        if (response.success) {
            Alert.success("Sauvegarde effectuée !")
        }
        else {
            Alert.error("Erreur lors de la sauvegarde des paramètres !")
        }

    }

    function FBhandleOldCarHz(e) {
        const hz = parseInt(e.target.value)
        setFBoldCarPostDelay(hz)
        setFBcreateOldCarPost(hz !== 0)

    }

    function IGhandleOldCarHz(e) {
        const hz = parseInt(e.target.value)
        setIGoldCarPostDelay(hz)
        setIGcreateOldCarPost(hz !== 0)
    }

    return (<div className="MainPage">
        {dealerInfos && <div className="Content">

            <div className="Title">
                <h1>Page de configuration </h1>
                {(dealerInfos.igToken || dealerInfos.fbToken) && <div className="Testmode">
                    <span>Activer le mode Test</span>
                    <Toggle isActive={testMode} setFct={setTestMode} />
                </div>}
            </div>

            <div className="Settings">
                <form className={testMode ? "Test" : "Prod"}>
                    <h2>Fonctionnalités</h2>
                    <h2>Facebook</h2>
                    <h2>Instagram</h2>
                    {testMode && !isMobile && <h2>Test</h2>}

                    <div className="Setting First">
                        <span className="SettingName First">Mettre en PAUSE les publications <ToolTip msg="Si cette option est activée, aucun post ne sera publié sur vos réseaux." /></span>
                    </div>

                    <Toggle isActive={FBpageIsPaused} setFct={setFBpageIsPaused} />
                    <Toggle isActive={IGpageIsPaused} setFct={setIGpageIsPaused} />
                    {!isMobile && testMode && <span></span>}
                        <div className="Setting">
                            <span className="SettingName">Créer un post quand un véhicule est ajouté à votre catalogue <ToolTip msg="Chaque véhicule ajouté à votre stock AutoScout fera l'objet d'un nouveau post." /></span>
                            <span></span>
                        </div>
                        <Toggle isActive={FBcreateNewCarPost} setFct={setFBcreateNewCarPost} />
                        <Toggle isActive={IGcreateNewCarPost} setFct={setIGcreateNewCarPost} />
                        
                        {testMode && <button id="0" onClick={testingPost}>Tester</button>}
                        {testMode && isMobile && <span />}
                        <div className="Setting">
                            <span className="SettingName">Créer une story quand un véhicule est ajouté à votre catalogue <ToolTip msg="Chaque véhicule ajouté à votre stock AutoScout fera l'objet d'une nouvelle story." /></span>
                        </div>

                        <Toggle isActive={FBcreateNewCarStory} setFct={setFBcreateNewCarStory} />
                        <Toggle isActive={IGcreateNewCarStory} setFct={setIGcreateNewCarStory} />

                        {testMode && <button id="6" onClick={testingPost}>Tester</button>}
                        {testMode && isMobile && <span />}

                        <div className="Setting">
                            <span className="SettingName">Créer un post quand un véhicule a été vendu <ToolTip msg="Quand un véhicule est retiré de votre catalogue il sera considéré comme vendu. Un post sera créé pour signaler la vente." /></span>
                        </div>
                        <Toggle isActive={FBcreateSoldCarPost} setFct={setFBcreateSoldCarPost} />
                        <Toggle isActive={IGcreateSoldCarPost} setFct={setIGcreateSoldCarPost} />

                        {testMode && <button id="1" onClick={testingPost}>Tester</button>}
                        {testMode && isMobile && <span />}

                        <div className="Setting">
                            <span className="SettingName">Créer un post quand une réduction a lieu sur un véhicule <ToolTip msg="Lorsque le prix d’un véhicule est diminué, un post est réalisé pour le mettre en avant." /></span>
                        </div>
                        <Toggle isActive={FBcreateDiscountCarPost} setFct={setFBcreateDiscountCarPost} />
                        <Toggle isActive={IGcreateDiscountCarPost} setFct={setIGcreateDiscountCarPost} />

                        {testMode && <button id="3" onClick={testingPost}>Tester</button>}
                        {testMode && isMobile && <span />}

                        <div className="Setting">
                            <span className="SettingName">Créer des posts de rappel <ToolTip msg="Si un véhicule est présent depuis longtemps dans votre catalogue mais n’a toujours pas trouvé preneur, un post sera créé toutes les X semaines afin de remettre l’annonce en avant." /></span>
                        </div>

                        <select value={FBoldCarPostDelay} onChange={FBhandleOldCarHz}>
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

                        <select value={IGoldCarPostDelay} onChange={IGhandleOldCarHz}>
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


                    <input onClick={handleButtonClick} type="Submit" className="Submit Primary" value={!isMobile ? "Sauvegarder les changements" : "Sauvegarder"}></input>

                </form>
            </div>

        </div>}
    </div>)
}

export default MainPage