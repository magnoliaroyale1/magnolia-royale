import {Container,Card,Table,Form,Tabs,Tab} from 'react-bootstrap';
import {useApiResource} from '../../hooks/useApi';
import {api} from '../../services/api';
import {AdminSidebar} from '../../components/AdminSidebar';
export function AdminInbox(){
 const {data:contacts}=useApiResource<any[]>('/admin/contacts',[]);const {data:reports}=useApiResource<any[]>('/admin/reports',[]);
 return <Container className="py-5"><div className="row"><div className="col-md-3"><AdminSidebar/></div><div className="col-md-9"><h2 className="font-serif text-olive">Contatos e denúncias</h2><Tabs defaultActiveKey="contacts" className="mb-3">
 <Tab eventKey="contacts" title="Contatos">{contacts.map(c=><Card className="mb-3" key={c.id}><Card.Body><h5>{c.name}</h5><small>{c.email}</small><p className="mt-2">{c.message}</p></Card.Body></Card>)}{!contacts.length&&<p>Nenhum contato recebido.</p>}</Tab>
 <Tab eventKey="reports" title="Denúncias">{reports.map(r=><Card className="mb-3" key={r.id}><Card.Body><h5>{r.clinicName}: {r.reason}</h5><p>{r.description}</p><Form.Select aria-label="Status da denúncia" value={r.status} onChange={e=>api(`/admin/reports/${r.id}`,'PATCH',{status:e.target.value}).catch(()=>{})}><option value="open">Aberta</option><option value="investigating">Em análise</option><option value="resolved">Resolvida</option></Form.Select></Card.Body></Card>)}</Tab>
 </Tabs></div></div></Container>;
}
