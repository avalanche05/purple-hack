import { Button, Col, Layout, Row, Typography, Upload } from 'antd';
import { Content, Header } from 'antd/es/layout/layout';
import { Link } from 'react-router-dom';
import { LogoutOutlined, UploadOutlined } from '@ant-design/icons';
import AuthService from '../api/AuthService';
import { useStores } from '../hooks/useStores';
import { observer } from 'mobx-react-lite';
import { Gantt, ViewMode } from 'gantt-task-react';
import 'gantt-task-react/dist/index.css';

const Home = observer(() => {
    const { rootStore } = useStores();

    return (
        <>
            <Layout style={{ background: '#ffffff' }}>
                <Header
                    style={{
                        position: 'sticky',
                        top: 0,
                        zIndex: 1,
                        width: '100%',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'end',
                        background: '#ffffff',
                        borderBottom: '1px solid #e8e8e8',
                    }}
                >
                    <Col>
                        <Link
                            onClick={() => {
                                AuthService.logout();

                                setTimeout(() => {
                                    window.location.href = '/login';
                                }, 100);
                            }}
                            to='/login'
                            style={{ marginLeft: 20 }}
                        >
                            <LogoutOutlined />
                        </Link>
                    </Col>
                </Header>
                <Content style={{ padding: '0 50px 50px 50px' }}>
                    <Row>
                        <Col>
                            <Typography.Title level={2}>Загрузка файла</Typography.Title>
                        </Col>
                    </Row>

                    <Row>
                        <Col>
                            <Upload
                                name='file'
                                beforeUpload={(file) => {
                                    rootStore.uploadFile(file);

                                    return false;
                                }}
                                accept='.json'
                                multiple={false}
                                maxCount={1}
                            >
                                <Button icon={<UploadOutlined />}>Загрузить JSON</Button>
                            </Upload>
                        </Col>
                    </Row>

                    {rootStore.uploadedGanttTasks && (
                        <>
                            <Row style={{ marginTop: 20 }}>
                                <Typography.Title level={2}>
                                    График из загруженного файла
                                </Typography.Title>
                            </Row>

                            <Gantt tasks={rootStore.uploadedGanttTasks} viewMode={ViewMode.Week} />

                            <Row>
                                <Typography.Title level={2}>Расчет</Typography.Title>
                            </Row>

                            <Row>
                                <Col>
                                    <Button
                                        type='primary'
                                        size='large'
                                        onClick={() => rootStore.calculate()}
                                        disabled={!rootStore.file}
                                        loading={rootStore.loading}
                                    >
                                        {rootStore.loading ? 'Файл обрабатывается' : 'Расчитать'}
                                    </Button>
                                </Col>
                            </Row>
                        </>
                    )}

                    {rootStore.calculatedGanttTasks && (
                        <>
                            <Row style={{ marginTop: 20 }}>
                                <Typography.Title level={2}>График после расчета</Typography.Title>
                            </Row>

                            <Gantt
                                tasks={rootStore.calculatedGanttTasks}
                                viewMode={ViewMode.Week}
                            />
                        </>
                    )}
                </Content>
            </Layout>
        </>
    );
});

export default Home;
