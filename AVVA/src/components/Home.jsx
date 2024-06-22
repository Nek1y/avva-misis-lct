import {useState, useEffect} from "react";
import UserService from "../services/user.service";
import DatePicker from "react-datepicker";
import {Bar, Line, Pie} from "react-chartjs-2";
import "react-datepicker/dist/react-datepicker.css";
import "chart.js/auto";
import { faker } from '@faker-js/faker';

const Home = () => {
    const [sources, setSources] = useState([]);
    const [content, setContent] = useState("");
    const [theme, setTheme] = useState("marketAnalysis");
    const [source, setSource] = useState("");
    const [startDate, setStartDate] = useState(new Date());
    const [endDate, setEndDate] = useState(new Date());
    const [llmModel, setLlmModel] = useState("ChatGPT");
    const [chartType, setChartType] = useState("bar");
    const [chartData, setChartData] = useState({
        labels: ["January", "February", "March", "April", "May", "June"],
        datasets: [
            {
                label: "Dataset 1",
                data: [65, 59, 80, 81, 56, 55],
                backgroundColor: "rgba(75, 192, 192, 0.6)",
                borderColor: "rgba(75, 192, 192, 1)",
                borderWidth: 1,
            },
        ],
    });

    const handleGenerate = () => {
        const n = {...chartData}
        n.datasets[0].data = new Array(faker.number.int(40)).fill(0).map(e => faker.number.int(150))
        n.labels = new Array(faker.number.int(12)).fill(0).map(e => faker.date.month())
        setChartData(JSON.parse(JSON.stringify(n)))
        console.log({
            theme,
            source,
            startDate,
            endDate,
            llmModel,
        });
    };

    const renderChart = () => {
        switch (chartType) {
            case "bar":
                return <Bar data={chartData}/>;
            case "line":
                return <Line data={chartData}/>;
            case "pie":
                return <Pie data={chartData}/>;
            default:
                return null;
        }
    };

    useEffect(() => {
        UserService.getPublicContent().then(
            (response) => {
                setContent(response.data);
            },
            (error) => {
                const _content =
                    (error.response && error.response.data) ||
                    error.message ||
                    error.toString();

                setContent(_content);
            }
        );
    }, []);

    return (
        <>
            {/*<div className="container">*/}
            {/*    <header className="jumbotron">*/}
            {/*        <h3>{content}</h3>*/}
            {/*    </header>*/}
            {/*</div>*/}
            <div className="app-container">
                <div className="form-section">
                    <h1 className="Zag">Создание нового отчета</h1>

                    <div className="section">
                        <h2>Тематика</h2>
                        <div>
                            <label>
                                <input
                                    type="radio"
                                    value="marketAnalysis"
                                    checked={theme === "marketAnalysis"}
                                    onChange={() => setTheme("marketAnalysis")}
                                />
                                Рыночные анализы
                            </label>
                            <label>
                                <input
                                    type="radio"
                                    value="financialAnalysis"
                                    checked={theme === "financialAnalysis"}
                                    onChange={() => setTheme("financialAnalysis")}
                                />
                                Финансовый анализ
                            </label>
                            <label>
                                <input
                                    type="radio"
                                    value="productComparison"
                                    checked={theme === "productComparison"}
                                    onChange={() => setTheme("productComparison")}

                                />
                                Сравнение продуктов
                            </label>
                            <label>
                                <input
                                    type="radio"
                                    value="technologyComparison"
                                    checked={theme === "technologyComparison"}
                                    onChange={() => setTheme("technologyComparison")}
                                />
                                Сравнение технологий
                            </label>
                            <label>
                                <input
                                    type="radio"
                                    value="competitorAnalysis"
                                    checked={theme === "competitorAnalysis"}
                                    onChange={() => setTheme("competitorAnalysis")}
                                    
                                />
                                Анализ конкурентов
                            </label>
                        </div>
                    </div>

                    <div className="section">
                        <h2>Источники</h2>
                        <input
                            type="text"
                            placeholder="Указать"
                            value={source}
                            onChange={(e) => setSource(e.target.value)}
                        />
                    </div>

                    <div className="section">
                        <h2>Временные рамки</h2>
                        <div>
                            <DatePicker
                                selected={startDate}
                                onChange={(date) => setStartDate(date)}
                            />
                            <DatePicker
                                selected={endDate}
                                onChange={(date) => setEndDate(date)}
                            />
                        </div>
                    </div>

                    <div className="section">
                        <h2>LLM модель</h2>
                        <div>
                            <label>
                                <input
                                    type="radio"
                                    value="ChatGPT"
                                    checked={llmModel === "ChatGPT"}
                                    onChange={() => setLlmModel("ChatGPT")}
                                />
                                ChatGPT
                            </label>
                            <label>
                                <input
                                    type="radio"
                                    value="AnotherModel"
                                    checked={llmModel === "AnotherModel"}
                                    onChange={() => setLlmModel("AnotherModel")}
                                />
                                Другая модель
                            </label>
                        </div>
                    </div>

                    <button onClick={handleGenerate}>Сгенерировать</button>
                </div>

                <div className="chart-section">
                <div className="sidebar">
                    <ul>
                        <li onClick={() => setChartType("bar")}>Столбчатая диаграмма</li>
                        <li onClick={() => setChartType("line")}>Линейная диаграмма</li>
                        <li onClick={() => setChartType("pie")}>Круговая диаграмма</li>
                        <li onClick={() => setChartType("text")}>Текстовый блок</li>
                        <li onClick={() => setChartType("table")}>Таблица</li>
                    </ul>
                </div>

                    {chartType === "text" && <div>Текстовый блок</div>}
                    {chartType === "table" && (
                        <table>
                            <thead>
                            <tr>
                                <th>Месяц</th>
                                <th>Значение</th>
                            </tr>
                            </thead>
                            <tbody>
                            {chartData.labels.map((label, index) => (
                                <tr key={index}>
                                    <td>{label}</td>
                                    <td>{chartData.datasets[0].data[index]}</td>
                                </tr>
                            ))}
                            </tbody>
                        </table>
                    )}
                    {chartType !== "text" && chartType !== "table" && renderChart()}
                </div>
            </div>
        </>
    );
};

export default Home;
