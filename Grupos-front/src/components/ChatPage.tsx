import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { messageService, Message } from '../services/messageService';
import { authService, User } from '../services/authService';
import { grupoService } from '../services/grupoService';
import { Grupo } from '../types';
import { Send, Image as ImageIcon, ArrowLeft, Loader2, Users, Settings, Plus, Hash, Shield, User as UserIcon, Trash2, Edit, X } from 'lucide-react';

const MemberItem: React.FC<{ user: any, userName?: string, onUpdateRole?: () => void, onRemove?: () => void, onStartDM?: () => void }> = ({ user, userName, onUpdateRole, onRemove, onStartDM }) => (
  <div className="flex items-center justify-between group px-2 py-1.5 rounded-xl hover:bg-indigo-50/50 transition-all duration-200">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center text-slate-500 font-bold text-xs uppercase border border-white shadow-sm ring-2 ring-transparent group-hover:ring-indigo-200 transition-all">
            {userName?.charAt(0) || <UserIcon size={14} />}
        </div>
        <div>
            <p className="text-xs font-bold text-slate-800 group-hover:text-indigo-900 transition-colors">{userName || `Usuario ${user.id_usuario}`}</p>
        </div>
      </div>
      <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-all transform translate-x-2 group-hover:translate-x-0">
        <button 
          onClick={onStartDM}
          className="p-1.5 bg-white shadow-sm border border-slate-100 text-slate-400 hover:text-indigo-600 hover:border-indigo-200 rounded-lg transition-all active:scale-90"
          title="Chat Privado"
        >
            <Send size={12} />
        </button>
        <button 
          onClick={onUpdateRole}
          className="p-1.5 bg-white shadow-sm border border-slate-100 text-slate-400 hover:text-indigo-600 hover:border-indigo-200 rounded-lg transition-all active:scale-90"
        >
            <Edit size={12} />
        </button>
        <button 
          onClick={onRemove}
          className="p-1.5 bg-white shadow-sm border border-slate-100 text-slate-400 hover:text-rose-600 hover:border-rose-200 rounded-lg transition-all active:scale-90"
        >
            <Trash2 size={12} />
        </button>
      </div>
  </div>
);

export const ChatPage: React.FC = () => {
  const { groupId } = useParams<{ groupId: string }>();
  const navigate = useNavigate();
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [currentGroup, setCurrentGroup] = useState<Grupo | null>(null);
  const [parentGroup, setParentGroup] = useState<Grupo | null>(null);
  const [subgroups, setSubgroups] = useState<Grupo[]>([]);
  const [groupUsers, setGroupUsers] = useState<any[]>([]);
  const [groupRoles, setGroupRoles] = useState<any[]>([]);
  const [userNames, setUserNames] = useState<Record<number, string>>({});
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [showSubgroupModal, setShowSubgroupModal] = useState(false);
  const [newSubgroupName, setNewSubgroupName] = useState('');
  const [isEditingGroup, setIsEditingGroup] = useState(false);
  const [allResources, setAllResources] = useState<any[]>([]);
  const [showRoleForm, setShowRoleForm] = useState(false);
  const [newRoleName, setNewRoleName] = useState('');
  const [editingRoleId, setEditingRoleId] = useState<string | null>(null);
  const [showUserModal, setShowUserModal] = useState(false);
  const [showInviteModal, setShowInviteModal] = useState(false);
  const [showDiscInviteModal, setShowDiscInviteModal] = useState(false);
  const [showImageModal, setShowImageModal] = useState<string | null>(null);
  
  const [inviteEmail, setInviteEmail] = useState('');

  const [selectedUsers, setSelectedUsers] = useState<string[]>([]);
  const [allUsers, setAllUsers] = useState<any[]>([]);
  const [parentGroupUsers, setParentGroupUsers] = useState<any[]>([]);
  const [myGroupsIds, setMyGroupsIds] = useState<Set<string>>(new Set());
  
  const [editGroupName, setEditGroupName] = useState('');
  const [editGroupDesc, setEditGroupDesc] = useState('');
  const [editGroupPrivado, setEditGroupPrivado] = useState(false);
  const [editGroupInvitacion, setEditGroupInvitacion] = useState(false);
  const [activeTab, setActiveRoleTab] = useState<'info' | 'roles'>('info');
  const panelRef = useRef<HTMLDivElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchMessages = async () => {
    if (!groupId) return;
    try {
      const msgs = await messageService.getMessages(groupId);
      setMessages([...msgs].reverse());
    } catch (err) {
      console.error('Error fetching messages', err);
    }
  };

  useEffect(() => {
    const initChat = async () => {
      const token = localStorage.getItem('token');
      if (!token || !groupId) {
        navigate('/login');
        return;
      }
      try {
        const [user, group, users, roles, resources, usersList, myGroups] = await Promise.all([
          authService.getProfile(token),
          grupoService.getById(groupId),
          messageService.getGroupUsers(groupId),
          grupoService.getRoles(groupId),
          grupoService.getAllResources(),
          authService.getAllUsers(),
          grupoService.getMyGroups()
        ]);
        
        setCurrentUser(user);
        setCurrentGroup(group);
        setGroupUsers(users);
        setGroupRoles(roles);
        setAllResources(resources);
        setAllUsers(usersList);
        setMyGroupsIds(new Set(myGroups.map(g => g.id_grupo)));

        // Si es un subgrupo, cargar el padre para el sidebar y discusiones

        const effectiveParentId = group.id_grupo_padre || group.id_grupo;
        
        const [pGroup, sGroups, pUsers] = await Promise.all([
          group.id_grupo_padre ? grupoService.getById(group.id_grupo_padre) : Promise.resolve(group),
          grupoService.getSubgroups(effectiveParentId),
          group.id_grupo_padre ? messageService.getGroupUsers(group.id_grupo_padre) : Promise.resolve([])
        ]);

        setParentGroup(pGroup);
        setSubgroups(sGroups);
        setParentGroupUsers(pUsers);
        
        await fetchMessages();
      } catch (err) {
        console.error(err);
        navigate('/login');
      } finally {
        setLoading(false);
      }
    };
    initChat();
  }, [groupId]);

  useEffect(() => {
    const interval = setInterval(fetchMessages, 3000);
    return () => clearInterval(interval);
  }, [groupId]);

  useEffect(scrollToBottom, [messages]);

  useEffect(() => {
    const unknownIds = messages
      .map(m => Number(m.sender_id))
      .filter(id => id !== currentUser?.user_id && !userNames[id]);
    
    const uniqueUnknownIds = Array.from(new Set(unknownIds));

    uniqueUnknownIds.forEach(async (id) => {
      if (isNaN(id)) return;
      try {
        const data = await authService.getUserById(id);
        setUserNames(prev => ({ ...prev, [id]: data.username }));
      } catch (err) {
        setUserNames(prev => ({ ...prev, [id]: `Usuario ${id}` }));
      }
    });

    if (Array.isArray(groupUsers)) {
      groupUsers.forEach(async (u) => {
        const id = Number(u.id_usuario);
        if (!userNames[id]) {
          try {
            const data = await authService.getUserById(id);
            setUserNames(prev => ({ ...prev, [id]: data.username }));
          } catch (err) {}
        }
      });
    }
  }, [messages, groupUsers, currentUser, userNames]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim() || !groupId || !currentUser) return;

    setSending(true);
    try {
      await messageService.sendMessage({
        chat_id: groupId,
        type: 'text',
        content: content,
        sender_id: currentUser.user_id
      });
      setContent('');
      await fetchMessages();
    } catch (err) {
      console.error(err);
    } finally {
      setSending(false);
    }
  };

  const handleCreateSubgroup = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSubgroupName.trim() || !parentGroup) return;
    
    try {
      await grupoService.create({
        nombre: newSubgroupName,
        id_grupo_padre: parentGroup.id_grupo,
        privado: parentGroup.privado
      });
      const sGroups = await grupoService.getSubgroups(parentGroup.id_grupo);
      setSubgroups(sGroups);
      setShowSubgroupModal(false);
      setNewSubgroupName('');
    } catch (err) {
      alert("Error al crear discusión");
    }
  };

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !groupId || !currentUser) return;

    try {
      const data = await messageService.uploadMedia(file, groupUsers.length);
      await messageService.sendMessage({
        chat_id: groupId,
        type: 'image',
        content: data.media_id,
        sender_id: currentUser.user_id
      });
      await fetchMessages();
    } catch (err) {
      console.error(err);
    }
  };

  const handleToggleEdit = () => {
    if (!isEditingGroup && currentGroup) {
      setEditGroupName(currentGroup.nombre);
      setEditGroupDesc(currentGroup.descripcion || '');
      setEditGroupPrivado(currentGroup.privado);
      setEditGroupInvitacion(currentGroup.requiere_invitacion);
    }
    setIsEditingGroup(!isEditingGroup);
    setActiveRoleTab('info');
  };

  const handleTogglePermission = async (roleId: string, resourceId: string, hasPermission: boolean) => {
    if (!groupId) return;
    try {
      if (hasPermission) {
        await grupoService.removePermission(groupId, roleId, resourceId);
      } else {
        await grupoService.assignPermission(groupId, roleId, resourceId);
      }
      const roles = await grupoService.getRoles(groupId);
      setGroupRoles(roles);
    } catch (err) {
      alert("Error al modificar permisos");
    }
  };

  const handleSaveRole = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!groupId || !newRoleName.trim()) return;
    try {
      if (editingRoleId) {
        await grupoService.updateRole(groupId, editingRoleId, newRoleName);
      } else {
        await grupoService.createRole(groupId, newRoleName);
      }
      const roles = await grupoService.getRoles(groupId);
      setGroupRoles(roles);
      setNewRoleName('');
      setEditingRoleId(null);
      setShowRoleForm(false);
    } catch (err) {
      alert("Error al gestionar rol");
    }
  };

  const handleDeleteRole = async (roleId: string) => {
    if (!groupId || !confirm("¿Eliminar este rol definitivamente?")) return;
    try {
      await grupoService.deleteRole(groupId, roleId);
      const roles = await grupoService.getRoles(groupId);
      setGroupRoles(roles);
    } catch (err) {
      alert("Error al eliminar rol");
    }
  };

  const handleStartDM = async (targetUser: any) => {
    if (!currentUser) return;
    try {
        const groupNameA = `${currentUser.username}-${targetUser.username}`;
        const groupNameB = `${targetUser.username}-${currentUser.username}`;
        
        // 0. Validar si ya existe una conversación entre ambos
        // Consultamos mis grupos para ver si ya hay uno con esos nombres
        const myGroups = await grupoService.getMyGroups();
        const existingDM = myGroups.find(g => g.nombre === groupNameA || g.nombre === groupNameB);

        if (existingDM) {
            setShowUserModal(false);
            navigate(`/chat/${existingDM.id_grupo}`);
            return;
        }

        // 1. Crear el grupo 1a1 si no existe
        const newGroup = await grupoService.create({
            nombre: groupNameA,
            descripcion: `Conversación privada entre ${currentUser.username} y ${targetUser.username}`,
            privado: true
        });

        // 2. Obtener los roles para este grupo
        let roles = [];
        for (let i = 0; i < 5; i++) {
            await new Promise(r => setTimeout(r, 500)); // Delay mayor para consistencia
            try {
                roles = await grupoService.getRoles(newGroup.id_grupo);
                if (roles.length > 0) break;
            } catch (e) {}
        }

        const adminRole = roles.find(r => r.nombre === 'Administrador');

        if (adminRole) {
            // 3. Añadir al otro usuario como Admin
            const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8002';
            await axios.post(`${API_URL}/users-groups/${newGroup.id_grupo}/usuarios`, {
                id_usuario: String(targetUser.id_usuario),
                id_rol_grupo: adminRole.id_rol_grupo,
                id_estado: 'ACTIVO'
            }, {
                headers: { 
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json'
                }
            });
        }

        setShowUserModal(false);
        navigate(`/chat/${newGroup.id_grupo}`);
    } catch (err) {
        console.error("Error iniciando DM:", err);
        alert("Error al iniciar conversación privada. Es posible que el grupo se haya creado pero hubo un problema al añadir al otro miembro.");
    }
  };

  const handleUpdateUserRole = async (userId: number) => {
    const roleName = prompt("Nombre del nuevo rol (ej: Moderador, Miembro):");
    if (!roleName || !groupId) return;
    
    const role = groupRoles.find(r => r.nombre.toLowerCase() === roleName.toLowerCase());
    if (!role) {
        alert("Rol no encontrado en el grupo");
        return;
    }

    try {
        await grupoService.updateUserRole(groupId, userId, role.id_rol_grupo);
        const users = await messageService.getGroupUsers(groupId);
        setGroupUsers(users);
    } catch (err: any) {
        alert(err.response?.data?.detail || "Error al cambiar rol");
    }
  };

  const handleRemoveUser = async (userId: number) => {
    if (!groupId || !confirm("¿Eliminar usuario del grupo?")) return;
    try {
        await grupoService.removeUser(groupId, userId);
        const users = await messageService.getGroupUsers(groupId);
        setGroupUsers(users);
    } catch (err) {
        alert("Error al eliminar usuario");
    }
  };

  const handleInviteByEmail = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inviteEmail.trim() || !groupId) return;

    try {
      // 1. Invitar vía gRPC (MS Grupos -> MS Auth)
      const user = await grupoService.inviteByEmail(groupId, inviteEmail.trim());
      
      // 2. Refrescar lista y cerrar
      const users = await messageService.getGroupUsers(groupId);
      setGroupUsers(users);
      setShowInviteModal(false);
      setInviteEmail('');
      alert(`Usuario ${user.username} agregado correctamente.`);
      
    } catch (err: any) {
      if (err.response?.status === 404) {
        alert("No se encontró ningún usuario con ese correo electrónico");
      } else {
        alert(err.response?.data?.detail || "Error al invitar usuario");
      }
    }
  };

  const handleUpdateGroup = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!groupId || !currentGroup) return;
    try {
      const updated = await grupoService.update(groupId, {
        nombre: editGroupName,
        descripcion: editGroupDesc,
        privado: editGroupPrivado,
        requiere_invitacion: editGroupInvitacion
      });
      setCurrentGroup(updated);
      setIsEditingGroup(false);
    } catch (err) {
      alert("Error al actualizar grupo");
    }
  };

  const handleWheel = (e: React.WheelEvent) => {
    if (!canManageRoles || !isEditingGroup) return;
    
    // Evitar cambio de pestaña si se está haciendo scroll dentro de la descripción
    const target = e.target as HTMLElement;
    if (target.tagName === 'TEXTAREA') {
        const txt = target as HTMLTextAreaElement;
        const isAtBottom = txt.scrollHeight - txt.scrollTop <= txt.clientHeight + 1;
        const isAtTop = txt.scrollTop <= 0;
        if (e.deltaY > 0 && !isAtBottom) return;
        if (e.deltaY < 0 && !isAtTop) return;
    }
    
    if (e.deltaY > 0 && activeTab === 'info') {
      setActiveRoleTab('roles');
    } 
    else if (e.deltaY < 0 && activeTab === 'roles') {
      const isAtTop = panelRef.current?.scrollTop === 0;
      if (isAtTop) {
        setActiveRoleTab('info');
      }
    }
  };

  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    if (!canManageRoles || !isEditingGroup) return;
    const threshold = 10;
    const isAtBottom = e.currentTarget.scrollHeight - e.currentTarget.scrollTop <= e.currentTarget.clientHeight + threshold;
    const isAtTop = e.currentTarget.scrollTop <= threshold;

    if (isAtBottom && activeTab === 'info') {
      setActiveRoleTab('roles');
      e.currentTarget.scrollTop = 0; 
    } else if (isAtTop && activeTab === 'roles') {
      setTimeout(() => {
        if (e.currentTarget.scrollTop <= threshold) {
          setActiveRoleTab('info');
        }
      }, 50);
    }
  };

  const canManageRoles = groupRoles.some(r => 
    (Array.isArray(groupUsers) ? groupUsers : []).find(u => 
      String(u.id_usuario) === String(currentUser?.user_id) && String(u.id_rol_grupo) === String(r.id_rol_grupo) && (r.permisos || []).includes('ROL_MNG')
    )
  );

  const canManageGroup = groupRoles.some(r => 
    (Array.isArray(groupUsers) ? groupUsers : []).find(u => 
      String(u.id_usuario) === String(currentUser?.user_id) && String(u.id_rol_grupo) === String(r.id_rol_grupo) && ((r.permisos || []).includes('GRP_MOD') || (r.permisos || []).includes('ROL_MNG'))
    )
  );

  const handleBulkInvite = async () => {
    if (!groupId || selectedUsers.length === 0) return;
    try {
        const roles = await grupoService.getRoles(groupId);
        const memberRole = roles.find(r => r.nombre === 'Miembro') || roles[roles.length - 1];
        
        for (const userId of selectedUsers) {
            await grupoService.addUserToGroup(groupId, Number(userId), memberRole.id_rol_grupo);
        }
        
        const users = await messageService.getGroupUsers(groupId);
        setGroupUsers(users);
        setShowDiscInviteModal(false);
        setSelectedUsers([]);
        alert("Miembros agregados exitosamente");
    } catch (err) {
        alert("Error al agregar algunos miembros");
    }
  };

  const handleJoinDisc = async (discId: string) => {
    try {
        await axios.post(`${import.meta.env.VITE_API_URL}/users-groups/${discId}/join`, {}, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        const myGroups = await grupoService.getMyGroups();
        setMyGroupsIds(new Set(myGroups.map(g => g.id_grupo)));
        navigate(`/chat/${discId}`);
    } catch (err) {
        alert("No puedes unirte a esta discusión");
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="animate-spin text-indigo-600" size={48} />
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-white overflow-hidden relative">
      {/* Modal de Imagen (Ver una vez) */}
      {showImageModal && (
        <div className="fixed inset-0 z-[100] bg-black/95 backdrop-blur-md flex flex-col items-center justify-center p-4">
            <button 
                onClick={() => setShowImageModal(null)}
                className="absolute top-6 right-6 text-white/50 hover:text-white transition-colors"
            >
                <X size={40} strokeWidth={1.5} />
            </button>
            <div className="max-w-4xl max-h-[80vh] relative group">
                <img 
                    src={messageService.getMediaUrl(showImageModal, currentUser?.user_id || 0)} 
                    alt="Ver una vez" 
                    className="max-w-full max-h-[80vh] rounded-lg shadow-2xl object-contain animate-in zoom-in-95 duration-300"
                />
                <div className="absolute -bottom-12 left-0 right-0 text-center">
                    <p className="text-white/60 text-xs font-bold uppercase tracking-[0.3em]">Esta foto se autodestruirá al cerrar</p>
                </div>
            </div>
        </div>
      )}

      {/* Modal de Invitación por Email */}
      {showInviteModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-sm overflow-hidden animate-in fade-in zoom-in duration-200">
            <div className="p-6 border-b border-slate-100 flex justify-between items-center">
              <h3 className="text-xl font-black text-slate-900">Invitar al Grupo</h3>
              <button onClick={() => setShowInviteModal(false)} className="text-slate-400 hover:text-slate-600">
                <X size={24} />
              </button>
            </div>
            <form onSubmit={handleInviteByEmail} className="p-6 space-y-4">
              <div>
                <label className="block text-[10px] font-black text-slate-400 uppercase mb-1">Correo Electrónico</label>
                <input
                  autoFocus
                  type="email"
                  required
                  value={inviteEmail}
                  onChange={(e) => setInviteEmail(e.target.value)}
                  placeholder="usuario@ejemplo.com"
                  className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm"
                />
              </div>
              <div className="flex gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setShowInviteModal(false)}
                  className="flex-1 py-3 px-4 rounded-xl text-sm font-bold text-slate-500 bg-slate-100 hover:bg-slate-200 transition-colors"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={!inviteEmail.trim()}
                  className="flex-1 py-3 px-4 rounded-xl text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 shadow-lg shadow-indigo-100 transition-all"
                >
                  Agregar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

        {/* Modal de Invitación a Discusión (desde Miembros del Padre) */}
      {showDiscInviteModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in duration-200">
            <div className="p-6 border-b border-slate-100 flex justify-between items-center">
              <div>
                <h3 className="text-xl font-black text-slate-900">Agregar Miembros</h3>
                <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Desde {parentGroup?.nombre}</p>
              </div>
              <button onClick={() => setShowDiscInviteModal(false)} className="text-slate-400 hover:text-slate-600">
                <X size={24} />
              </button>
            </div>
            <div className="p-4 max-h-[50vh] overflow-y-auto space-y-2 custom-scrollbar">
               {parentGroupUsers
                .filter(pu => !groupUsers.some(gu => String(gu.id_usuario) === String(pu.id_usuario)))
                .map(u => (
                 <label
                   key={u.id_usuario}
                   className="w-full flex items-center justify-between p-3 rounded-xl hover:bg-indigo-50 transition-all cursor-pointer group"
                 >
                   <div className="flex items-center gap-3">
                     <div className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center text-indigo-600 font-bold group-hover:bg-white transition-colors">
                        {userNames[u.id_usuario]?.charAt(0).toUpperCase() || <UserIcon size={18} />}
                     </div>
                     <div>
                        <p className="text-sm font-bold text-slate-800">{userNames[u.id_usuario] || `Usuario ${u.id_usuario}`}</p>
                     </div>
                   </div>
                   <input
                    type="checkbox"
                    checked={selectedUsers.includes(String(u.id_usuario))}
                    onChange={(e) => {
                        if (e.target.checked) setSelectedUsers([...selectedUsers, String(u.id_usuario)]);
                        else setSelectedUsers(selectedUsers.filter(id => id !== String(u.id_usuario)));
                    }}
                    className="rounded-full text-indigo-600 focus:ring-indigo-500 w-5 h-5 border-slate-300 transition-all appearance-none checked:bg-indigo-600"
                   />
                 </label>
               ))}
               {parentGroupUsers.filter(pu => !groupUsers.some(gu => String(gu.id_usuario) === String(pu.id_usuario))).length === 0 && (
                   <p className="text-center py-8 text-xs font-bold text-slate-400 uppercase tracking-widest">Todos los miembros del padre ya están aquí</p>
               )}
            </div>
            <div className="p-6 border-t border-slate-100 flex gap-3">
                <button onClick={() => setShowDiscInviteModal(false)} className="flex-1 py-3 text-sm font-bold text-slate-500 bg-slate-100 rounded-xl">Cancelar</button>
                <button 
                    disabled={selectedUsers.length === 0}
                    onClick={handleBulkInvite}
                    className="flex-1 py-3 text-sm font-bold text-white bg-indigo-600 rounded-xl shadow-lg shadow-indigo-100 disabled:opacity-50"
                >
                    Agregar ({selectedUsers.length})
                </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal de Miembros para DM */}
      {showUserModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in duration-200">
            <div className="p-6 border-b border-slate-100 flex justify-between items-center">
              <h3 className="text-xl font-black text-slate-900">Iniciar Chat Privado</h3>
              <button onClick={() => setShowUserModal(false)} className="text-slate-400 hover:text-slate-600">
                <X size={24} />
              </button>
            </div>
            <div className="p-4 max-h-[60vh] overflow-y-auto space-y-2 custom-scrollbar">
               {allUsers.filter(u => String(u.id_usuario) !== String(currentUser?.user_id)).map(u => (
                 <button
                   key={u.id_usuario}
                   onClick={() => handleStartDM(u)}
                   className="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-indigo-50 transition-all text-left group"
                 >
                   <div className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center text-indigo-600 font-bold group-hover:bg-white transition-colors">
                     {u.username.charAt(0).toUpperCase()}
                   </div>
                   <div>
                     <p className="text-sm font-bold text-slate-800">{u.username}</p>
                     <p className="text-[10px] text-slate-500">{u.email}</p>
                   </div>
                 </button>
               ))}
            </div>
          </div>
        </div>
      )}

      {/* Modal de Creación de Subgrupo */}
      {showSubgroupModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in duration-200">
            <div className="p-6 border-b border-slate-100 flex justify-between items-center">
              <h3 className="text-xl font-black text-slate-900">Nueva Discusión</h3>
              <button onClick={() => setShowSubgroupModal(false)} className="text-slate-400 hover:text-slate-600">
                <X size={24} />
              </button>
            </div>
            <form onSubmit={handleCreateSubgroup} className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-bold text-slate-700 mb-2">Nombre de la discusión</label>
                <input
                  autoFocus
                  type="text"
                  value={newSubgroupName}
                  onChange={(e) => setNewSubgroupName(e.target.value)}
                  placeholder="Ej: anuncios-importantes"
                  className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm"
                />
              </div>
              <p className="text-[10px] text-slate-400 font-medium">Esta discusión será visible para todos los miembros del grupo {parentGroup?.nombre}.</p>
              <div className="flex gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setShowSubgroupModal(false)}
                  className="flex-1 py-3 px-4 rounded-xl text-sm font-bold text-slate-500 bg-slate-100 hover:bg-slate-200 transition-colors"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={!newSubgroupName.trim()}
                  className="flex-1 py-3 px-4 rounded-xl text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 shadow-lg shadow-indigo-100 transition-all"
                >
                  Crear
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Sidebar Izquierda: Subgrupos/Discusiones */}
      <aside className="w-64 bg-slate-50 border-r border-slate-200 flex flex-col">
        <div className="p-4 border-b border-slate-200 bg-white flex justify-between items-center">
          <h3 className="font-bold text-slate-700 flex items-center gap-2 truncate pr-2">
            <Hash size={18} className="flex-shrink-0" /> {parentGroup?.nombre}
          </h3>
          <button 
            onClick={() => setShowSubgroupModal(true)} 
            className="p-1.5 hover:bg-indigo-50 rounded-lg text-indigo-600 transition-colors"
            title="Nueva Discusión"
          >
            <Plus size={20} />
          </button>
        </div>
        
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {/* Discusión Principal Fijada */}
          <button
            onClick={() => navigate(`/chat/${parentGroup?.id_grupo}`)}
            className={`w-full text-left px-3 py-2.5 rounded-xl text-sm font-black transition-all flex items-center gap-2 mb-2 ${
              groupId === parentGroup?.id_grupo 
                ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-100' 
                : 'text-slate-900 bg-white border border-slate-200 hover:border-indigo-300'
            }`}
          >
            <Hash size={16} className={groupId === parentGroup?.id_grupo ? 'opacity-100' : 'text-indigo-600'} />
            <span className="truncate">General</span>
          </button>

          <div className="px-3 pt-4 pb-2">
            <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Tus Discusiones</p>
          </div>

          {subgroups.filter(sg => myGroupsIds.has(sg.id_grupo)).map(sg => (
            <button
              key={sg.id_grupo}
              onClick={() => navigate(`/chat/${sg.id_grupo}`)}
              className={`w-full text-left px-3 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${
                groupId === sg.id_grupo 
                  ? 'bg-indigo-50 text-indigo-700' 
                  : 'text-slate-600 hover:bg-white hover:text-indigo-600'
              }`}
            >
              <Hash size={14} className="opacity-50 flex-shrink-0" />
              <span className="truncate">{sg.nombre}</span>
            </button>
          ))}

          {subgroups.filter(sg => !myGroupsIds.has(sg.id_grupo) && !sg.privado).length > 0 && (
            <>
                <div className="px-3 pt-6 pb-2">
                    <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Otras Discusiones</p>
                </div>
                {subgroups.filter(sg => !myGroupsIds.has(sg.id_grupo) && !sg.privado).map(sg => (
                    <div key={sg.id_grupo} className="flex items-center gap-1 group/disc px-1">
                        <button
                            disabled
                            className="flex-1 text-left px-3 py-2 rounded-lg text-sm font-medium text-slate-400 flex items-center gap-2"
                        >
                            <Hash size={14} className="opacity-30" />
                            <span className="truncate">{sg.nombre}</span>
                        </button>
                        <button 
                            onClick={() => handleJoinDisc(sg.id_grupo)}
                            className="px-2 py-1 bg-indigo-50 text-indigo-600 rounded-md text-[10px] font-bold opacity-0 group-hover/disc:opacity-100 transition-all hover:bg-indigo-600 hover:text-white"
                        >
                            Unirse
                        </button>
                    </div>
                ))}
            </>
          )}
          
          {subgroups.length === 0 && (
            <p className="text-[10px] text-slate-400 text-center mt-4 uppercase font-bold tracking-widest opacity-60">Sin otras discusiones</p>
          )}
        </div>

        <div className="p-4 border-t border-slate-200 bg-slate-100/50">
          <button onClick={() => navigate('/')} className="flex items-center gap-2 text-xs font-bold text-slate-500 hover:text-indigo-600 transition-colors w-full">
            <ArrowLeft size={14} /> Volver a Comunidades
          </button>
        </div>
      </aside>

      {/* Centro: Chat */}
      <main className="flex-1 flex flex-col bg-white">
        <header className="px-6 py-4 border-b border-slate-200 flex justify-between items-center bg-white/80 backdrop-blur-md sticky top-0 z-10">
          <div className="min-w-0">
            <h2 className="text-lg font-black text-slate-900 flex items-center gap-2 truncate">
              {currentGroup?.id_grupo_padre ? <Hash size={20} className="text-slate-400" /> : <Shield size={20} className="text-indigo-600" />}
              {currentGroup?.id_grupo === parentGroup?.id_grupo ? 'General' : currentGroup?.nombre}
            </h2>
            <p className="text-[10px] font-bold text-indigo-600 uppercase tracking-widest truncate">
              {currentGroup?.id_grupo === parentGroup?.id_grupo ? 'Canal Principal' : `Discusión en ${parentGroup?.nombre}`}
            </p>
          </div>
          <div className="flex items-center gap-3 ml-4">
             <div className="flex flex-col items-end">
               <span className="text-[10px] font-black text-slate-400 uppercase tracking-tighter leading-none">Conectado como</span>
               <span className="text-xs font-bold text-slate-900">{currentUser?.username}</span>
             </div>
             <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white text-xs font-black">
               {currentUser?.username.charAt(0).toUpperCase()}
             </div>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] bg-fixed">
          {messages.map((msg, i) => {
            const isMe = msg.sender_id === currentUser?.user_id;
            const senderName = isMe ? 'Tú' : (userNames[msg.sender_id] || `Usuario ${msg.sender_id}`);
            
            return (
              <div key={i} className={`flex ${isMe ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[85%] rounded-xl px-3 py-2 shadow-sm ${
                  isMe ? 'bg-indigo-600 text-white rounded-tr-none' : 'bg-white text-slate-800 border border-slate-200 rounded-tl-none'
                }`}>
                  {!isMe && <p className="text-[10px] font-black uppercase mb-0.5 opacity-70 tracking-wider">{senderName}</p>}
                  {msg.type === 'text' ? (
                    <p className="text-chat leading-snug whitespace-pre-wrap break-words font-medium">{msg.content}</p>
                  ) : (
                    <button 
                        disabled={msg.status?.read_by?.some((id: any) => String(id) === String(currentUser?.user_id))}
                        onClick={() => {
                            setShowImageModal(msg.content);
                            if (msg._id) {
                                axios.put(`${import.meta.env.VITE_MSG_URL}/messages/${msg._id}/read`, {}, {
                                    headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
                                }).then(() => fetchMessages());
                            }
                        }}
                        className={`flex items-center gap-3 px-4 py-3 rounded-xl border transition-all ${
                            msg.status?.read_by?.some((id: any) => String(id) === String(currentUser?.user_id))
                            ? 'bg-slate-100 border-slate-200 text-slate-400 cursor-not-allowed opacity-60'
                            : isMe 
                              ? 'bg-indigo-700/50 border-indigo-400/30 text-white hover:bg-indigo-700' 
                              : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
                        }`}
                    >
                        <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                            msg.status?.read_by?.some((id: any) => String(id) === String(currentUser?.user_id))
                            ? 'bg-slate-200 text-slate-400'
                            : isMe ? 'bg-indigo-500' : 'bg-indigo-100 text-indigo-600'
                        }`}>
                            <ImageIcon size={20} />
                        </div>
                        <div className="text-left">
                            <p className="text-[11px] font-black uppercase tracking-widest leading-none mb-1">
                                {msg.status?.read_by?.some((id: any) => String(id) === String(currentUser?.user_id)) ? 'Foto vista' : 'Foto'}
                            </p>
                            <p className="text-[10px] opacity-70 font-bold">
                                {msg.status?.read_by?.some((id: any) => String(id) === String(currentUser?.user_id)) ? 'Ya no puedes abrirla' : 'Haz clic para ver una vez'}
                            </p>
                        </div>
                    </button>
                  )}
                  <p className={`text-[9px] mt-1 font-bold text-right ${isMe ? 'text-indigo-200' : 'text-slate-400'}`}>
                    {msg.timestamp ? new Date(msg.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : ''}
                  </p>
                </div>
              </div>
            );
          })}
          <div ref={messagesEndRef} />
        </div>

        <footer className="p-4 bg-white border-t border-slate-200">
          <form onSubmit={handleSend} className="max-w-4xl mx-auto flex gap-3 items-center">
            <label className="p-2 text-slate-400 hover:text-indigo-600 transition-colors cursor-pointer rounded-lg hover:bg-slate-50">
              <ImageIcon size={22} />
              <input type="file" className="hidden" accept="image/*" onChange={handleImageUpload} />
            </label>
            <input
              type="text"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder={`Mensaje en #${currentGroup?.id_grupo === parentGroup?.id_grupo ? 'general' : currentGroup?.nombre}...`}
              className="flex-1 bg-slate-100 border-none rounded-xl px-4 py-3 focus:ring-2 focus:ring-indigo-500 text-sm transition-all placeholder:text-slate-400"
            />
            <button
              type="submit"
              disabled={sending || !content.trim()}
              className="bg-indigo-600 text-white p-3 rounded-xl hover:bg-indigo-700 disabled:opacity-50 transition-all shadow-lg shadow-indigo-100 flex items-center justify-center group"
            >
              <Send size={20} className="group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
            </button>
          </form>
        </footer>
      </main>

      {/* Sidebar Derecha: Administración */}
      <aside 
        className={`${isEditingGroup ? 'w-96' : 'w-80'} bg-white border-l border-slate-200 flex flex-col transition-all duration-300`}
        onWheel={handleWheel}
      >
        <div className="p-6 border-b border-slate-200">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-black text-slate-900 uppercase tracking-tighter flex items-center gap-2">
              <Settings size={18} className="text-slate-400" /> {isEditingGroup ? (activeTab === 'roles' ? 'Roles y Permisos' : 'Configuración') : 'Gestión'}
            </h3>
            {canManageGroup && (
              <button 
                onClick={handleToggleEdit}
                className={`p-2 rounded-lg transition-colors ${isEditingGroup ? 'bg-indigo-600 text-white' : 'hover:bg-slate-100 text-slate-500'}`}
                title={isEditingGroup ? "Cerrar Edición" : "Editar Grupo"}
              >
                {isEditingGroup ? <X size={16} /> : <Edit size={16} />}
              </button>
            )}
          </div>

          {!isEditingGroup ? (
            <div className="space-y-3 animate-in fade-in duration-300">
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 group/desc relative overflow-hidden transition-all duration-300 hover:bg-white hover:shadow-md">
                  <p className="text-[10px] font-black text-slate-400 uppercase mb-1">Descripción</p>
                  <p className="text-xs text-slate-600 leading-relaxed break-words line-clamp-[6] group-hover/desc:line-clamp-none transition-all duration-500">
                    {currentGroup?.descripcion || 'Sin descripción'}
                  </p>
              </div>
              <div className="flex gap-2">
                  <div className={`flex-1 p-2 rounded-lg text-center border ${currentGroup?.privado ? 'bg-amber-50 border-amber-100 text-amber-600' : 'bg-emerald-50 border-emerald-100 text-emerald-600'}`}>
                    <p className="text-[9px] font-black uppercase tracking-widest">{currentGroup?.privado ? 'Privado' : 'Público'}</p>
                  </div>
                  {canManageRoles && (
                    <button 
                      onClick={() => { 
                        setIsEditingGroup(true); 
                        setActiveRoleTab('roles');
                        setEditGroupName(currentGroup?.nombre || '');
                        setEditGroupDesc(currentGroup?.descripcion || '');
                        setEditGroupPrivado(currentGroup?.privado || false);
                        setEditGroupInvitacion(currentGroup?.requiere_invitacion || false);
                      }}
                      className="flex-1 p-2 rounded-lg bg-indigo-50 border border-indigo-100 text-indigo-600 hover:bg-indigo-100 transition-colors"
                    >
                      <p className="text-[9px] font-black uppercase tracking-widest flex items-center justify-center gap-1">
                          <Shield size={10} /> Roles
                      </p>
                    </button>
                  )}
              </div>
            </div>
          ) : null}
        </div>

        <div 
          ref={panelRef}
          onScroll={handleScroll}
          className="flex-1 overflow-y-auto custom-scrollbar"
        >
          {isEditingGroup ? (
            <div className="p-6">
              <form onSubmit={handleUpdateGroup} className="space-y-6">
                {activeTab === 'info' ? (
                  <div className="space-y-4 animate-in slide-in-from-right-5 duration-300">
                    <div>
                      <label className="block text-[10px] font-black text-slate-400 uppercase mb-1">Nombre</label>
                      <input 
                        type="text"
                        value={editGroupName}
                        onChange={(e) => setEditGroupName(e.target.value)}
                        className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs font-bold focus:ring-2 focus:ring-indigo-500 transition-all"
                      />
                    </div>
                    <div>
                      <label className="block text-[10px] font-black text-slate-400 uppercase mb-1">Descripción</label>
                      <textarea 
                        value={editGroupDesc}
                        onChange={(e) => setEditGroupDesc(e.target.value)}
                        className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium focus:ring-2 focus:ring-indigo-500 transition-all h-[45vh] min-h-[200px] overflow-y-auto custom-scrollbar resize-none leading-relaxed"
                        placeholder="Describe el propósito de esta comunidad..."
                      />
                    </div>
                    <div className="space-y-2">
                      <label className="flex items-center gap-3 cursor-pointer group">
                        <input 
                          type="checkbox"
                          checked={editGroupPrivado}
                          onChange={(e) => setEditGroupPrivado(e.target.checked)}
                          className="rounded-full text-indigo-600 focus:ring-indigo-500 w-5 h-5 border-slate-300 transition-all cursor-pointer appearance-none checked:bg-indigo-600"
                        />
                        <span className="text-xs font-black text-slate-600 uppercase tracking-widest group-hover:text-indigo-600 transition-colors">Grupo Privado</span>
                      </label>
                      <label className="flex items-center gap-3 cursor-pointer group">
                        <input 
                          type="checkbox"
                          checked={editGroupInvitacion}
                          onChange={(e) => setEditGroupInvitacion(e.target.checked)}
                          className="rounded-full text-indigo-600 focus:ring-indigo-500 w-5 h-5 border-slate-300 transition-all cursor-pointer appearance-none checked:bg-indigo-600"
                        />
                        <span className="text-xs font-black text-slate-600 uppercase tracking-widest group-hover:text-indigo-600 transition-colors">Requiere Invitación</span>
                      </label>
                    </div>
                    {canManageRoles && (
                      <div className="pt-4 flex flex-col items-center gap-2 text-slate-300 animate-pulse">
                        <p className="text-[8px] font-bold uppercase tracking-[0.2em]">Desliza para gestionar roles</p>
                        <Shield size={16} />
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="space-y-4 animate-in slide-in-from-bottom-2 duration-300">
                    <div className="flex items-center justify-between">
                      <h4 className="text-[10px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
                        <Shield size={14} /> Gestión de Roles
                      </h4>
                      <button 
                        type="button"
                        onClick={() => { setShowRoleForm(true); setEditingRoleId(null); setNewRoleName(''); }}
                        className="p-1 hover:bg-indigo-50 rounded text-indigo-600 transition-colors"
                      >
                        <Plus size={16} />
                      </button>
                    </div>

                    {showRoleForm && (
                      <div className="p-4 bg-slate-50 rounded-xl border border-indigo-100 shadow-inner">
                        <input 
                          autoFocus
                          type="text"
                          placeholder="Nombre del rol"
                          value={newRoleName}
                          onChange={(e) => setNewRoleName(e.target.value)}
                          className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-xs font-bold mb-3 focus:ring-2 focus:ring-indigo-500"
                        />
                        <div className="flex gap-2">
                          <button type="button" onClick={() => setShowRoleForm(false)} className="flex-1 py-2 text-[10px] font-bold text-slate-500 bg-white border border-slate-200 rounded-lg">Cancelar</button>
                          <button type="button" onClick={handleSaveRole} className="flex-1 py-2 text-[10px] font-bold text-white bg-indigo-600 rounded-lg">Guardar</button>
                        </div>
                      </div>
                    )}

                    <div className="space-y-4 max-h-[500px] overflow-y-auto pr-1 custom-scrollbar">
                      {Array.isArray(groupRoles) && groupRoles
                        .filter(role => role.nombre !== 'Administrador')
                        .map(role => (
                        <div key={role.id_rol_grupo} className="p-3 bg-white border border-slate-100 rounded-xl shadow-sm space-y-3">
                          <div className="flex items-center justify-between">
                            <p className="text-xs font-black text-slate-800 uppercase tracking-tighter">{role.nombre}</p>
                            <div className="flex gap-1">
                               <button 
                                type="button"
                                onClick={() => { setEditingRoleId(role.id_rol_grupo); setNewRoleName(role.nombre); setShowRoleForm(true); }}
                                className="p-1 text-slate-400 hover:text-indigo-600 transition-colors"
                               >
                                 <Edit size={12} />
                               </button>
                               {role.nombre !== 'Administrador' && (
                                 <button 
                                  type="button"
                                  onClick={() => handleDeleteRole(role.id_rol_grupo)}
                                  className="p-1 text-slate-400 hover:text-rose-600 transition-colors"
                                 >
                                   <Trash2 size={12} />
                                 </button>
                               )}
                            </div>
                          </div>
                          
                          <div className="grid grid-cols-1 gap-3">
                            {allResources.map(res => {
                              const hasPerm = (role.permisos || []).includes(res.id_recurso);
                              return (
                                <label key={res.id_recurso} className="flex items-center justify-between cursor-pointer group/perm py-0.5">
                                   <span className="text-[12px] font-semibold text-slate-600 group-hover/perm:text-indigo-700 transition-colors">{res.nombre_recurso}</span>
                                   <input 
                                    type="checkbox"
                                    checked={hasPerm}
                                    onChange={() => handleTogglePermission(role.id_rol_grupo, res.id_recurso, hasPerm)}
                                    className="rounded-full text-indigo-600 focus:ring-indigo-500 w-4.5 h-4.5 border-slate-300 transition-all cursor-pointer appearance-none checked:bg-indigo-600"
                                   />
                                </label>
                              );
                            })}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </form>
            </div>
          ) : (
            <div className="p-4 animate-in fade-in duration-300">
              <h4 className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mb-6 flex items-center gap-2">
                <Users size={14} /> Miembros — {Array.isArray(groupUsers) ? groupUsers.length : 0}
              </h4>
              
              <div className="space-y-4">
                {Array.isArray(groupRoles) && groupRoles.length > 0 ? (
                  [...groupRoles]
                    .sort((a, b) => {
                      const weights: Record<string, number> = { 'Administrador': 1, 'Moderador': 2, 'Miembro': 3 };
                      return (weights[a.nombre] || 99) - (weights[b.nombre] || 99);
                    })
                    .map(role => {
                      const usersInRole = (Array.isArray(groupUsers) ? groupUsers : []).filter(u => String(u.id_rol_grupo) === String(role.id_rol_grupo));
                      if (usersInRole.length === 0) return null;

                      return (
                        <div key={role.id_rol_grupo} className="space-y-1">
                          <div className="flex items-center gap-2 px-1 mb-1">
                            <p className="text-[9px] font-black text-indigo-400 uppercase tracking-[0.3em]">{role.nombre}</p>
                            <span className="h-px flex-1 bg-slate-100"></span>
                          </div>
                          
                          <div className="space-y-0.5">
                            {usersInRole.map((u, i) => (
                              <MemberItem 
                                key={i} 
                                user={u} 
                                userName={userNames[u.id_usuario]} 
                                onStartDM={() => {
                                  const target = allUsers.find(au => String(au.id_usuario) === String(u.id_usuario));
                                  if (target) handleStartDM(target);
                                }}
                                onUpdateRole={() => handleUpdateUserRole(u.id_usuario)}
                                onRemove={() => handleRemoveUser(u.id_usuario)}
                              />
                            ))}
                          </div>
                        </div>
                      );
                    })
                ) : (
                  <div className="space-y-1">
                    <div className="flex items-center gap-2 px-1 mb-1">
                      <p className="text-[9px] font-black text-slate-400 uppercase tracking-[0.3em]">Todos los Miembros</p>
                      <span className="h-px flex-1 bg-slate-100"></span>
                    </div>
                    <div className="space-y-0.5">
                    {Array.isArray(groupUsers) && groupUsers.map((u, i) => (
                      <MemberItem 
                        key={i} 
                        user={u} 
                        userName={userNames[u.id_usuario]} 
                        onStartDM={() => {
                          const target = allUsers.find(au => String(au.id_usuario) === String(u.id_usuario));
                          if (target) handleStartDM(target);
                        }}
                        onUpdateRole={() => handleUpdateUserRole(u.id_usuario)}
                        onRemove={() => handleRemoveUser(u.id_usuario)}
                      />
                    ))}
                  </div>

                  </div>
                )}

                {Array.isArray(groupRoles) && groupRoles.length > 0 && Array.isArray(groupUsers) && groupUsers.some(u => !groupRoles.find(r => String(r.id_rol_grupo) === String(u.id_rol_grupo))) && (
                   <div className="space-y-1">
                      <div className="flex items-center gap-2 px-1 mb-1">
                        <p className="text-[9px] font-black text-rose-300 uppercase tracking-[0.3em]">Otros</p>
                        <span className="h-px flex-1 bg-slate-100"></span>
                      </div>
                      <div className="space-y-0.5">
                        {Array.isArray(groupUsers) && groupUsers.filter(u => !groupRoles.find(r => String(r.id_rol_grupo) === String(u.id_rol_grupo))).map((u, i) => (
                          <MemberItem 
                              key={i} 
                              user={u} 
                              userName={userNames[u.id_usuario]} 
                              onStartDM={() => {
                                const target = allUsers.find(au => String(au.id_usuario) === String(u.id_usuario));
                                if (target) handleStartDM(target);
                              }}
                              onUpdateRole={() => handleUpdateUserRole(u.id_usuario)}
                              onRemove={() => handleRemoveUser(u.id_usuario)}
                          />
                        ))}

                      </div>
                   </div>
                )}
              </div>
            </div>
          )}
        </div>

        {isEditingGroup && (
          <div className="p-6 border-t border-slate-200 bg-white">
            <button 
              onClick={handleUpdateGroup}
              className="w-full py-3 bg-indigo-600 text-white rounded-xl text-xs font-black uppercase tracking-widest hover:bg-indigo-700 shadow-lg shadow-indigo-100 transition-all active:scale-[0.98]"
            >
              Guardar Cambios
            </button>
          </div>
        )}
        
        {!isEditingGroup && (
        <div className="p-6 border-t border-slate-200 flex flex-col gap-2">
           <button 
            onClick={() => {
                if (currentGroup?.id_grupo_padre) {
                    setShowDiscInviteModal(true);
                } else {
                    setShowInviteModal(true);
                }
            }}
            className="w-full py-3 bg-indigo-600 text-white rounded-xl text-xs font-black uppercase tracking-widest hover:bg-indigo-700 transition-all shadow-lg shadow-indigo-100 active:scale-[0.98]"
           >
              Invitar Miembro
           </button>
           <button 
            onClick={() => setShowUserModal(true)}
            className="w-full py-3 bg-slate-900 text-white rounded-xl text-xs font-black uppercase tracking-widest hover:bg-black transition-all shadow-lg shadow-slate-200 active:scale-[0.98]"
           >
              Iniciar Chat Privado (DM)
           </button>
        </div>

        )}
      </aside>
    </div>
  );
};
