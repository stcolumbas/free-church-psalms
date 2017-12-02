module Main exposing (..)

import Html exposing (Html, program)
import Html.Attributes as A
import Html.Events as E


-- Model


type alias Model =
    { step : Step
    , fileFormat : FileFormat
    , colour : Maybe Colour
    , underlined : Maybe Underlined
    , ratioOrResolution : Maybe RatioOrResolution
    }


initialModel : Model
initialModel =
    { step = Intro
    , fileFormat = None
    , colour = Nothing
    , underlined = Nothing
    , ratioOrResolution = Nothing
    }


type Step
    = Intro
    | ChooseFileFormat
    | ChooseOptions FileFormat


type FileFormat
    = None
    | PlainText
    | PDF
    | PowerPoint
    | ProPresenter


type Colour
    = BlackOnWhite
    | WhiteOnBlack


type RatioOrResolution
    = Ratio Ratio
    | Resolution Resolution


type Ratio
    = Four_Three
    | Sixteen_Nine


type Resolution
    = R_1080_1920
    | R_720_1280
    | R_768_1024


type alias Underlined =
    Bool



-- Update


type Msg
    = GetStartedClicked
    | FormatClicked FileFormat
    | ColourClicked Colour
    | UnderlinedClicked Underlined
    | RatioClicked Ratio
    | ResolutionClicked Resolution


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    let
        model_ =
            case msg of
                GetStartedClicked ->
                    { model | step = ChooseFileFormat }

                FormatClicked format ->
                    if model.fileFormat == format then
                        model
                    else
                        { model
                            | step = ChooseOptions format
                            , fileFormat = format
                            , colour = Nothing
                            , underlined = Nothing
                            , ratioOrResolution = Nothing
                        }

                ColourClicked colour ->
                    { model | colour = Just colour }

                UnderlinedClicked u ->
                    { model | underlined = Just u }

                RatioClicked ratio ->
                    case model.fileFormat of
                        ProPresenter ->
                            { model | fileFormat = None }

                        PlainText ->
                            { model | fileFormat = None }

                        _ ->
                            { model | ratioOrResolution = Just <| Ratio ratio }

                ResolutionClicked resolution ->
                    case model.fileFormat of
                        PowerPoint ->
                            { model | fileFormat = None }

                        PlainText ->
                            { model | fileFormat = None }

                        _ ->
                            { model | ratioOrResolution = Just <| Resolution resolution }
    in
    model_ ! []



-- View


view : Model -> Html Msg
view model =
    Html.div [ A.class "w-screen h-screen flex flex-wrap p-8" ]
        [ Html.div [ A.class "md:w-1/2 md:ml-auto" ]
            [ Html.h1 [ A.class "my-8" ] [ Html.text "Psalms for Screens" ]
            , viewHelp model
            ]
        , Html.div [ A.class "md:w-1/3 md:mr-auto" ]
            [ Html.div [ A.class "sm:h-8 md:h-64" ] []
            , finalLink model
            , Html.div [ A.class "h-8" ] []
            ]
        ]


viewHelp : Model -> Html Msg
viewHelp model =
    case model.step of
        Intro ->
            Html.div [] [ introView True ]

        ChooseFileFormat ->
            Html.div []
                [ introView False
                , chooseFormat model.fileFormat
                ]

        ChooseOptions format ->
            Html.div []
                [ introView False
                , chooseFormat format
                , case format of
                    PlainText ->
                        Html.text ""

                    _ ->
                        chooseOptions model format
                ]


introView : Bool -> Html Msg
introView showButton =
    Html.div [ A.class "" ]
        [ Html.div [ A.class "text-left" ]
            [ Html.p [] [ Html.text "You can find both Sing Psalms and Scottish Psalter slides for your screens here. As an increasing number of churches use screens for their worship instead of printed psalters, these resources are here to make it easier for you to display the psalm words quickly and easily." ]
            , Html.br [] []
            , Html.p [] [ Html.text "The psalms are available in a full range of formats, so you can choose the precise version which best suits your needs. Just click the button below to begin." ]
            , Html.br [] []
            , Html.p []
                [ Html.text "If you find a problem, need help or want to request an additional format, please contact "
                , Html.a [ A.href "mailto:help@stcsfc.org?Subect=Psalm%20Slides" ] [ Html.text "help@stcsfc.org" ]
                , Html.text "."
                ]
            , Html.br [] []
            , Html.p [] [ Html.text "\"Sing Psalms\" words are copyright of the Free Church of Scotland and are reproduced here with permission from the Psalmody Committee. These files are distributed, solely, for non-commercial use." ]
            , Html.br [] []
            , Html.p []
                [ Html.text "For more information about our psalm singing tradition, and for full copyright permissions, please click "
                , Html.a [ A.href "https://freechurch.org/resources/praise/sing-psalms" ] [ Html.text "here" ]
                , Html.text "."
                ]
            , spacer
            ]
        , if showButton then
            Html.div [ A.class "text-center py-8" ]
                [ button
                    [ E.onClick GetStartedClicked
                    , A.class "bg-dark"
                    ]
                    [ Html.text "Get Started" ]
                ]
          else
            Html.text ""
        ]


spacer : Html Msg
spacer =
    Html.div [ A.class "sm:h-8 md:h-24" ] []


button : List (Html.Attribute Msg) -> List (Html Msg) -> Html Msg
button attrs nodes =
    Html.button
        (attrs
            ++ [ A.class buttonClasses ]
        )
        nodes


buttonClasses : String
buttonClasses =
    "text-white text-lg font-bold py-4 px-6 rounded shadow max-w-md mx-1"


selectedButton : Bool -> List (Html.Attribute Msg) -> List (Html Msg) -> Html Msg
selectedButton bool attrs nodes =
    if bool then
        button ([ A.class "bg-dark text-stcs-red" ] ++ attrs) nodes
    else
        button ([ A.class "bg-dark" ] ++ attrs) nodes


optionListClasses : String
optionListClasses =
    "pt-4"


chooseFormat : FileFormat -> Html Msg
chooseFormat format =
    Html.div []
        [ Html.h3 [ A.class "my-2" ] [ Html.text "Pick a Format" ]
        , selectedButton (format == PlainText) [ E.onClick <| FormatClicked PlainText ] [ Html.text "Plain Text" ]
        , selectedButton (format == PDF) [ E.onClick <| FormatClicked PDF ] [ Html.text "PDF" ]
        , selectedButton (format == PowerPoint) [ E.onClick <| FormatClicked PowerPoint ] [ Html.text "PowerPoint" ]
        , selectedButton (format == ProPresenter) [ E.onClick <| FormatClicked ProPresenter ] [ Html.text "ProPresenter" ]
        ]


chooseOptions : Model -> FileFormat -> Html Msg
chooseOptions model format =
    Html.div []
        [ Html.div [ A.class optionListClasses ]
            [ Html.h4 [ A.class "my-2" ] [ Html.text "Colour" ]
            , selectedButton (maybeBool model.colour BlackOnWhite) [ E.onClick <| ColourClicked BlackOnWhite ] [ Html.text "Black on White" ]
            , selectedButton (maybeBool model.colour WhiteOnBlack) [ E.onClick <| ColourClicked WhiteOnBlack ] [ Html.text "White on Black" ]
            ]
        , Html.div [ A.class optionListClasses ]
            [ Html.h4 [ A.class "my-2" ] [ Html.text "Underlined" ]
            , selectedButton (maybeBool model.underlined True) [ E.onClick <| UnderlinedClicked True ] [ Html.text "With underlining" ]
            , selectedButton (maybeBool model.underlined False) [ E.onClick <| UnderlinedClicked False ] [ Html.text "Without underlining" ]
            ]
        , resolutionOrRatioList format model.ratioOrResolution
        ]


maybeBool : Maybe a -> a -> Bool
maybeBool maybeX1 x2 =
    case maybeX1 of
        Nothing ->
            False

        Just x1 ->
            x1 == x2


resolutionOrRatioList : FileFormat -> Maybe RatioOrResolution -> Html Msg
resolutionOrRatioList format ratioOrResolution =
    case ( format, ratioOrResolution ) of
        ( None, _ ) ->
            Html.text ""

        ( PlainText, _ ) ->
            Html.text ""

        ( PDF, Just ror ) ->
            case ror of
                Ratio r ->
                    ratiosList <| Just r

                _ ->
                    Html.text ""

        ( PDF, Nothing ) ->
            ratiosList Nothing

        ( PowerPoint, Just ror ) ->
            case ror of
                Ratio r ->
                    ratiosList <| Just r

                _ ->
                    Html.text ""

        ( PowerPoint, Nothing ) ->
            ratiosList Nothing

        ( ProPresenter, Just ror ) ->
            case ror of
                Resolution r ->
                    resolutionsList <| Just r

                _ ->
                    Html.text ""

        ( ProPresenter, Nothing ) ->
            resolutionsList Nothing


ratiosList : Maybe Ratio -> Html Msg
ratiosList ratio =
    Html.div [ A.class optionListClasses ]
        [ Html.h4 [ A.class "my-2" ] [ Html.text "Aspect Ratio" ]
        , Html.p [] [ Html.text "" ]
        , selectedButton (maybeBool ratio Four_Three) [ E.onClick <| RatioClicked Four_Three ] [ Html.text "4x3" ]
        , selectedButton (maybeBool ratio Sixteen_Nine) [ E.onClick <| RatioClicked Sixteen_Nine ] [ Html.text "16x9 (widescreen)" ]
        ]


resolutionsList : Maybe Resolution -> Html Msg
resolutionsList res =
    Html.div [ A.class optionListClasses ]
        [ Html.h4 [ A.class "my-2" ] [ Html.text "Screen Resolution" ]
        , Html.p [] [ Html.text "" ]
        , selectedButton (maybeBool res R_1080_1920) [ E.onClick <| ResolutionClicked R_1080_1920 ] [ Html.text "1080x1920" ]
        , selectedButton (maybeBool res R_720_1280) [ E.onClick <| ResolutionClicked R_720_1280 ] [ Html.text "720x1280" ]
        , selectedButton (maybeBool res R_768_1024) [ E.onClick <| ResolutionClicked R_768_1024 ] [ Html.text "768x1024" ]
        ]


finalLink : Model -> Html Msg
finalLink model =
    let
        link =
            makeLink model
    in
    case link of
        Nothing ->
            Html.text ""

        Just l ->
            Html.a [ A.class ("w-full bg-dark " ++ buttonClasses), A.href l ] [ Html.text "Click to download your Psalms" ]


type Link
    = Link FileFormat Colour Underlined RatioOrResolution


makeLink : Model -> Maybe String
makeLink model =
    case model.fileFormat of
        None ->
            Nothing

        PlainText ->
            Maybe.map3 (Link model.fileFormat)
                (Just BlackOnWhite)
                (Just True)
                (Just <| Ratio Four_Three)
                |> Maybe.map link2String

        _ ->
            Maybe.map3 (Link model.fileFormat)
                model.colour
                model.underlined
                model.ratioOrResolution
                |> Maybe.map link2String


link2String : Link -> String
link2String (Link format colour underlined ratioOrResolution) =
    case format of
        PlainText ->
            "/output/PlainText.Zip"

        _ ->
            "/output/"
                ++ formatString format
                ++ "/"
                ++ ratioOrResolutionString ratioOrResolution
                ++ "_"
                ++ colourString colour
                ++ underlinedString underlined
                ++ ".zip"


underlinedString : Bool -> String
underlinedString u =
    if u then
        "_underlined"
    else
        ""


colourString : Colour -> String
colourString c =
    case c of
        BlackOnWhite ->
            "b_w"

        WhiteOnBlack ->
            "w_b"


formatString : FileFormat -> String
formatString format =
    case format of
        None ->
            ""

        PlainText ->
            "PlainText"

        PowerPoint ->
            "PowerPoint"

        PDF ->
            "PDF"

        ProPresenter ->
            "ProPresenter5"


ratioOrResolutionString : RatioOrResolution -> String
ratioOrResolutionString r =
    case r of
        Ratio Four_Three ->
            "4x3"

        Ratio Sixteen_Nine ->
            "16x9"

        Resolution R_1080_1920 ->
            "1080x1920"

        Resolution R_720_1280 ->
            "720x1280"

        Resolution R_768_1024 ->
            "768x1024"



-- Main


main : Program Never Model Msg
main =
    program
        { init = init
        , view = view
        , update = update
        , subscriptions = \_ -> Sub.none
        }


init : ( Model, Cmd Msg )
init =
    ( initialModel, Cmd.none )
