import { Button, Col, Layout, Upload } from 'antd';
import { Content, Header } from 'antd/es/layout/layout';
import { Link } from 'react-router-dom';
import { LogoutOutlined, UploadOutlined } from '@ant-design/icons';
import AuthService from '../api/AuthService';
import { useStores } from '../hooks/useStores';
import { observer } from 'mobx-react-lite';
import { Gantt } from 'gantt-task-react';
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
                <Content style={{ padding: '0 50px' }}>
                    <Upload
                        name='file'
                        beforeUpload={(file) => {
                            rootStore.uplaodFile(file);

                            return false;
                        }}
                        accept='.json'
                    >
                        <Button icon={<UploadOutlined />}>Загрузить JSON</Button>
                    </Upload>

                    {rootStore.ganttTasks && <Gantt tasks={rootStore.ganttTasks} />}
                </Content>
            </Layout>
        </>
    );
});

export default Home;
