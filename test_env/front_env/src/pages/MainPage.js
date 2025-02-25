import { useEffect, useState, useContext } from 'react'
import "../styles/main.scss"
import FacebookLoginButton from '../components/FacebookLoginButton'
import * as Api from "../utils/Api.js"
import { AuthContext } from '../context/AuthContext.js'
import Alert from '../components/Alert.js'

function MainPage() {
    const { logoutUser } = useContext(AuthContext)

    const [enablePageManagemenent, setEnablePageManagement] = useState()

    const [enablePostNewCar, setEnablePostNewCar] = useState()
    const [enablePostSoldCar, setEnablePostSoldCar] = useState()

    const [enablePostOldCar, setEnablePostOldCar] = useState()
    const [oldCarHz, setOldCarHz] = useState()

    const [enablePostDiscount, setEnablePostDiscount] = useState()
    const [enableModifiedPost, setEnableModifiedPost] = useState()

    const [enablePostStockSummary, setEnablePostStockSummary] = useState()
    const [summaryHz, setSummaryHz] = useState()

    const [dealerInfos, setDealerInfos] = useState()

    async function testingPost(e) {
        e.preventDefault()
        const success = (await Api.fetchPost("/api/testing/", { "scenario": parseInt(e.target.id) })).success
        if (success){
            Alert.success("Le post a bien été créé.")
        }
        else{
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

    return (<div className="MainPage">
        {dealerInfos && <div className="Content">
            <h1>AutoShare</h1>
            <h2>Synchronisez votre stock <span>Autoscout24</span> avec vos réseaux sociaux, sans rien faire.</h2>
            <div className="Settings">
                <form>
                    <b>Fonctionnalités</b>
                    <b>Activé</b>
                    <b>Test</b>

                    <label>Activer la gestion de ma page</label>
                    <input checked={enablePageManagemenent} onChange={() => setEnablePageManagement(!enablePageManagemenent)} type="checkbox"></input>
                    <span></span>
                    {enablePageManagemenent &&
                        <>
                            <label>
                                Créer un post quand un véhicule est ajouté à votre catalogue

                            </label>
                            <input
                                type="checkbox"
                                checked={enablePostNewCar}
                                onChange={() => setEnablePostNewCar(!enablePostNewCar)}
                            />
                            <button id="0" onClick={testingPost}>Tester</button>

                            <label>
                                Créer un post quand un véhicule a été vendu

                            </label>
                            <input
                                type="checkbox"
                                checked={enablePostSoldCar}
                                onChange={() => setEnablePostSoldCar(!enablePostSoldCar)}
                            />
                            <button id="1" onClick={testingPost}>Tester</button>


                            <label>
                                Créer un post quand un véhicule présent dans le catalogue depuis <b>{oldCarHz}</b> semaines n'a pas encore été vendu

                            </label>
                            <input
                                type="checkbox"
                                checked={enablePostOldCar}
                                onChange={() => setEnablePostOldCar(!enablePostOldCar)}
                            />
                            <button id="2" onClick={testingPost}>Tester</button>
                            {enablePostOldCar ?
                                <>
                                    <label className="Secondary">
                                        Nombre de semaines
                                    </label>
                                    <select value={oldCarHz} onChange={(e) => setOldCarHz(e.target.value)}>
                                        <option value="1">1</option>
                                        <option value="2">2</option>
                                        <option value="3">3</option>
                                        <option value="4">4</option>
                                        <option value="5">5</option>
                                        <option value="6">6</option>
                                        <option value="7">7</option>
                                        <option value="8">8</option>
                                        <option value="9">9</option>
                                        <option value="10">10</option>
                                        <option value="11">11</option>
                                        <option value="12">12</option>
                                    </select> </>:<><span/><span/></>}
                            <span></span>



                            <label>
                                Créer un post quand une réduction a lieu sur un véhicule

                            </label>
                            <input
                                type="checkbox"
                                checked={enablePostDiscount}
                                onChange={() => setEnablePostDiscount(!enablePostDiscount)}
                            />
                            <button id="3" onClick={testingPost}>Tester</button>

                            <label>
                                Créer un post quand une modification de la fiche technique d'un véhicule a lieu

                            </label>
                            <input
                                type="checkbox"
                                checked={enableModifiedPost}
                                onChange={() => setEnableModifiedPost(!enableModifiedPost)}
                            />
                            <button id="4" onClick={testingPost}>Tester</button>

                            <label>
                                Créer un post récapitulatif du stock toutes les <b>{summaryHz}</b> semaines

                            </label>
                            <input
                                type="checkbox"
                                checked={enablePostStockSummary}
                                onChange={() => setEnablePostStockSummary(!enablePostStockSummary)}
                            />
                            <button id="5" onClick={testingPost}>Tester</button>

                            {enablePostStockSummary ? <>
                                <label className="Secondary">
                                    Nombre de semaines
                                </label>
                                <select value={summaryHz} onChange={(e) => setSummaryHz(e.target.value)}>
                                    <option value="1">1</option>
                                    <option value="2">2</option>
                                    <option value="3">3</option>
                                    <option value="4">4</option>
                                    <option value="5">5</option>
                                    <option value="6">6</option>
                                    <option value="7">7</option>
                                    <option value="8">8</option>
                                    <option value="9">9</option>
                                    <option value="10">10</option>
                                    <option value="11">11</option>
                                    <option value="12">12</option>
                                </select> </>:<><span/><span/></>}

                        </>
                    }
                    <input onClick={handleButtonClick} type="Submit" value="Sauvegarder les changements"></input>
                </form>
            </div>

        </div>}
    </div>)


}

export default MainPage