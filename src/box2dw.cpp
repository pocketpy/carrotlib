#include "box2dw.hpp"

namespace pkpy{

void PyBody::_register(VM* vm, PyObject* mod, PyObject* type){
    vm->bind(type, "__new__(cls, world: World, node=None, with_callback=True)",
        [](VM* vm, ArgsView args){
            PyWorld& world = CAST(PyWorld&, args[1]);
            PyObject* node = args[2];
            PyObject* obj = vm->heap.gcnew<PyBody>(PyBody::_type(vm));
            PyBody& body = _CAST(PyBody&, obj);
            b2BodyDef def;
            def.type = b2_dynamicBody;
            // a weak reference to this object
            def.userData.pointer = reinterpret_cast<uintptr_t>(obj);
            body.body = world.world.CreateBody(&def);
            body.node_like = node;
            body.with_callback = CAST(bool, args[3]);
            return obj;
        });

    PY_PROPERTY(PyBody, "type: int", _b2Body, GetType, SetType)
    PY_PROPERTY(PyBody, "gravity_scale: float", _b2Body, GetGravityScale, SetGravityScale)
    PY_PROPERTY(PyBody, "fixed_rotation: bool", _b2Body, IsFixedRotation, SetFixedRotation)
    PY_PROPERTY(PyBody, "enabled: bool", _b2Body, IsEnabled, SetEnabled)
    PY_PROPERTY(PyBody, "bullet: bool", _b2Body, IsBullet, SetBullet)
    
    PY_READONLY_PROPERTY(PyBody, "mass: float", _b2Body, GetMass)
    PY_READONLY_PROPERTY(PyBody, "inertia: float", _b2Body, GetInertia)

    PY_PROPERTY(PyBody, "position: vec2", _, get_position, set_position)
    PY_PROPERTY(PyBody, "rotation: float", _, get_rotation, set_rotation)
    PY_PROPERTY(PyBody, "velocity: vec2", _, get_velocity, set_velocity)
    PY_PROPERTY(PyBody, "angular_velocity: float", _b2Body, GetAngularVelocity, SetAngularVelocity)
    PY_PROPERTY(PyBody, "damping: float", _b2Body, GetLinearDamping, SetLinearDamping)
    PY_PROPERTY(PyBody, "angular_damping: float", _b2Body, GetAngularDamping, SetAngularDamping)

    PY_PROPERTY(PyBody, "density: float", _b2Fixture, GetDensity, SetDensity)
    PY_PROPERTY(PyBody, "friction: float", _b2Fixture, GetFriction, SetFriction)
    PY_PROPERTY(PyBody, "restitution: float", _b2Fixture, GetRestitution, SetRestitution)
    PY_PROPERTY(PyBody, "restitution_threshold: float", _b2Fixture, GetRestitutionThreshold, SetRestitutionThreshold)
    PY_PROPERTY(PyBody, "is_sensor: bool", _b2Fixture, IsSensor, SetSensor)

    vm->bind(type, "set_box_shape(self, hx: float, hy: float)",
        [](VM* vm, ArgsView args){
            PyBody& body = CAST(PyBody&, args[0]);
            float hx = CAST(float, args[1]);
            float hy = CAST(float, args[2]);
            b2PolygonShape shape;
            shape.SetAsBox(hx, hy);
            body._set_b2Fixture(body.body->CreateFixture(&shape, 1.0f));
            return vm->None;
        });

    vm->bind(type, "set_circle_shape(self, radius: float)",
        [](VM* vm, ArgsView args){
            PyBody& body = CAST(PyBody&, args[0]);
            float radius = CAST(float, args[1]);
            b2CircleShape shape;
            shape.m_radius = radius;
            body._set_b2Fixture(body.body->CreateFixture(&shape, 1.0f));
            return vm->None;
        });

    vm->bind(type, "set_polygon_shape(self, points: list[vec2])",
        [](VM* vm, ArgsView args){
            PyBody& body = CAST(PyBody&, args[0]);
            List& points = CAST(List&, args[1]);
            if(points.size() < 3 || points.size() > b2_maxPolygonVertices){
                vm->ValueError("invalid vertices count");
            }
            b2PolygonShape shape;
            std::vector<b2Vec2> vertices;
            for(auto& point : points){
                Vec2 vec = CAST(Vec2, point);
                vertices.push_back(b2Vec2(vec.x, vec.y));
            }
            shape.Set(vertices.data(), vertices.size());
            body._set_b2Fixture(body.body->CreateFixture(&shape, 1.0f));
            return vm->None;
        });

    vm->bind(type, "set_chain_shape(self, points: list[vec2])",
        [](VM* vm, ArgsView args){
            PyBody& body = CAST(PyBody&, args[0]);
            List& points = CAST(List&, args[1]);
            if(points.size() < 3){
                vm->ValueError("invalid vertices count");
            }
            b2ChainShape shape;
            std::vector<b2Vec2> vertices;
            for(auto& point : points){
                Vec2 vec = CAST(Vec2, point);
                vertices.push_back(b2Vec2(vec.x, vec.y));
            }
            shape.CreateLoop(vertices.data(), vertices.size());
            body._set_b2Fixture(body.body->CreateFixture(&shape, 1.0f));
            return vm->None;
        });

    // methods
    _bind(vm, type, "apply_force(self, force: vec2, point: vec2)", &PyBody::apply_force);
    _bind(vm, type, "apply_force_to_center(self, force: vec2)", &PyBody::apply_force_to_center);
    _bind(vm, type, "apply_torque(self, torque: float)", &PyBody::apply_torque);
    _bind(vm, type, "apply_impulse(self, impulse: vec2, point: vec2)", &PyBody::apply_impulse);
    _bind(vm, type, "apply_impulse_to_center(self, impulse: vec2)", &PyBody::apply_impulse_to_center);
    _bind(vm, type, "apply_angular_impulse(self, impulse: float)", &PyBody::apply_angular_impulse);

    // get_node
    vm->bind(type, "get_node(self)", [](VM* vm, ArgsView args){
        const PyBody& body = CAST(PyBody&, args[0]);
        return body.node_like;
    });

    // get_contacts
    vm->bind(type, "get_contacts(self) -> list[Body]", [](VM* vm, ArgsView args){
        PyBody& self = CAST(PyBody&, args[0]);
        b2ContactEdge* edge = self.body->GetContactList();
        List list;
        while(edge){
            b2Fixture* fixtureB = edge->contact->GetFixtureB();
            b2Body* bodyB = fixtureB->GetBody();
            list.push_back(get_body_object(bodyB));
            edge = edge->next;
        }
        return VAR(std::move(list));
    });

    // destroy
    vm->bind(type, "destroy(self)", [](VM* vm, ArgsView args){
        PyBody& body = CAST(PyBody&, args[0]);
        body._is_destroyed = true;  // mark as destroyed
        return vm->None;
    });
}

// def draw_polygon(self, vertices: list[vec2], color: vec4): ...
// def draw_solid_polygon(self, vertices: list[vec2], color: vec4): ...
// def draw_circle(self, center: vec2, radius: float, color: vec4): ...
// def draw_solid_circle(self, center: vec2, radius: float, axis: vec2, color: vec4): ...
// def draw_segment(self, p1: vec2, p2: vec2, color: vec4): ...
// def draw_transform(self, position: vec2, rotation: float): ...
// def draw_point(self, p: vec2, size: float, color: vec4): ...

static Vec4 color_to_vec4(const b2Color& color){
    return Vec4(color.r, color.g, color.b, color.a);
}

void PyDebugDraw::DrawPolygon(const b2Vec2* vertices, int32 vertexCount, const b2Color& color){
    DEF_SNAME(draw_polygon);
    List v(vertexCount);
    for(int i = 0; i < vertexCount; i++) v[i] = VAR(vertices[i]);
    PyObject* col = VAR(color_to_vec4(color));
    vm->call_method(draw_like, draw_polygon, VAR(std::move(v)), col);
}

void PyDebugDraw::DrawSolidPolygon(const b2Vec2* vertices, int32 vertexCount, const b2Color& color){
    DEF_SNAME(draw_solid_polygon);
    List v(vertexCount);
    for(int i = 0; i < vertexCount; i++) v[i] = VAR(vertices[i]);
    PyObject* col = VAR(color_to_vec4(color));
    vm->call_method(draw_like, draw_solid_polygon, VAR(std::move(v)), col);
}

void PyDebugDraw::DrawCircle(const b2Vec2& center, float radius, const b2Color& color){
    DEF_SNAME(draw_circle);
    PyObject* col = VAR(color_to_vec4(color));
    vm->call_method(draw_like, draw_circle, VAR(center), VAR(radius), col);
}

void PyDebugDraw::DrawSolidCircle(const b2Vec2& center, float radius, const b2Vec2& axis, const b2Color& color){
    DEF_SNAME(draw_solid_circle);
    PyObject* col = VAR(color_to_vec4(color));
    vm->call_method(draw_like, draw_solid_circle, VAR(center), VAR(radius), VAR(axis), col);
}

void PyDebugDraw::DrawSegment(const b2Vec2& p1, const b2Vec2& p2, const b2Color& color){
    DEF_SNAME(draw_segment);
    PyObject* col = VAR(color_to_vec4(color));
    vm->call_method(draw_like, draw_segment, VAR(p1), VAR(p2), col);
}

void PyDebugDraw::DrawTransform(const b2Transform& xf){
    DEF_SNAME(draw_transform);
    vm->call_method(draw_like, draw_transform, VAR(xf.p), VAR(xf.q.GetAngle()));
}

void PyDebugDraw::DrawPoint(const b2Vec2& p, float size, const b2Color& color){
    DEF_SNAME(draw_point);
    PyObject* col = VAR(color_to_vec4(color));
    vm->call_method(draw_like, draw_point, VAR(p), VAR(size), col);
}

void add_module_box2d(VM* vm){
    PyObject* mod = vm->new_module("box2d");
    PyBody::register_class(vm, mod);
    PyWorld::register_class(vm, mod);
}

struct MyRayCastCallback: b2RayCastCallback{
    PK_ALWAYS_PASS_BY_POINTER(MyRayCastCallback)

    VM* vm;
    List result;
    MyRayCastCallback(VM* vm): vm(vm) {}
 
    float ReportFixture(b2Fixture* fixture, const b2Vec2& point, const b2Vec2& normal, float fraction){
        result.push_back(get_body_object(fixture->GetBody()));
        // if(only_one) return 0;
        return fraction;
    }
};

struct MyBoxCastCallback: b2QueryCallback{
    PK_ALWAYS_PASS_BY_POINTER(MyBoxCastCallback)

    VM* vm;
    List result;
    MyBoxCastCallback(VM* vm): vm(vm) {}

    bool ReportFixture(b2Fixture* fixture) override{
        result.push_back(get_body_object(fixture->GetBody()));
        return true;
    }
};

void PyContactListener::_contact_f(b2Contact* contact, StrName name){
    PyObject* a = get_body_object(contact->GetFixtureA()->GetBody());
    PyObject* b = get_body_object(contact->GetFixtureB()->GetBody());
    PyBody& bodyA = PK_OBJ_GET(PyBody, a);
    PyBody& bodyB = PK_OBJ_GET(PyBody, b);
    PyObject* self;
    PyObject* f;
    f = vm->get_unbound_method(bodyA.node_like, name, &self, false);
    if(f != nullptr) vm->call_method(self, f, b);
    f = vm->get_unbound_method(bodyB.node_like, name, &self, false);
    if(f != nullptr) vm->call_method(self, f, a);
}

/****************** PyWorld ******************/
PyWorld::PyWorld(VM* vm): world(b2Vec2(0, 0)), _contact_listener(vm), _debug_draw(vm){
    _debug_draw.draw_like = vm->None;
    world.SetAllowSleeping(true);
    world.SetAutoClearForces(true);
    world.SetContactListener(&_contact_listener);
    world.SetDebugDraw(&_debug_draw);
}

void PyWorld::_register(VM* vm, PyObject* mod, PyObject* type){
    vm->bind(type, "__new__(cls)", [](VM* vm, ArgsView args){
        return vm->heap.gcnew<PyWorld>(PyWorld::_type(vm), vm);
    });

    // gravity
    vm->bind_property(type, "gravity: vec2", [](VM* vm, ArgsView args){
        PyWorld& self = _CAST(PyWorld&, args[0]);
        return VAR(self.world.GetGravity());
    }, [](VM* vm, ArgsView args){
        PyWorld& self = _CAST(PyWorld&, args[0]);
        self.world.SetGravity(CAST(b2Vec2, args[1]));
        return vm->None;
    });

    vm->bind(type, "get_bodies(self) -> list[Body]", [](VM* vm, ArgsView args){
        PyWorld& self = _CAST(PyWorld&, args[0]);
        List list;
        b2Body* p = self.world.GetBodyList();
        while(p != nullptr){
            list.push_back(get_body_object(p));
            p = p->GetNext();
        }
        return VAR(std::move(list));
    });

    vm->bind(type, "ray_cast(self, start: vec2, end: vec2) -> list[Body]", [](VM* vm, ArgsView args){
        auto _lock = vm->heap.gc_scope_lock();
        PyWorld& self = _CAST(PyWorld&, args[0]);
        b2Vec2 start = CAST(b2Vec2, args[1]);
        b2Vec2 end = CAST(b2Vec2, args[2]);
        MyRayCastCallback callback(vm);
        self.world.RayCast(&callback, start, end);
        return VAR(std::move(callback.result));
    });

    vm->bind(type, "box_cast(self, lower: vec2, upper: vec2) -> list[Body]", [](VM* vm, ArgsView args){
        auto _lock = vm->heap.gc_scope_lock();
        PyWorld& self = _CAST(PyWorld&, args[0]);
        b2AABB aabb;
        aabb.lowerBound = CAST(b2Vec2, args[1]);
        aabb.upperBound = CAST(b2Vec2, args[2]);
        MyBoxCastCallback callback(vm);
        self.world.QueryAABB(&callback, aabb);
        return VAR(std::move(callback.result));
    });

    vm->bind(type, "point_cast(self, point: vec2) -> list[Body]", [](VM* vm, ArgsView args){
        auto _lock = vm->heap.gc_scope_lock();
        PyWorld& self = _CAST(PyWorld&, args[0]);
        b2AABB aabb;
        aabb.lowerBound = CAST(b2Vec2, args[1]);
        aabb.upperBound = CAST(b2Vec2, args[1]);
        MyBoxCastCallback callback(vm);
        self.world.QueryAABB(&callback, aabb);
        return VAR(std::move(callback.result));
    });

    vm->bind(type, "step(self, dt: float, velocity_iterations: int, position_iterations: int)",
        [](VM* vm, ArgsView args){
            // disable gc during step for safety
            auto _lock = vm->heap.gc_scope_lock();

            PyWorld& self = _CAST(PyWorld&, args[0]);
            float dt = CAST(float, args[1]);
            int velocity_iterations = CAST(int, args[2]);
            int position_iterations = CAST(int, args[3]);

            auto f = [](VM* vm, b2Body* p, StrName name){
                while(p != nullptr){
                    PyObject* body_obj = get_body_object(p);
                    PyBody& body = _CAST(PyBody&, body_obj);
                    if(body.with_callback && !body._is_destroyed){
                        if(body.node_like != vm->None){
                            vm->call_method(body.node_like, name);
                        }
                    }
                    p = p->GetNext();
                }
            };

            DEF_SNAME(on_box2d_pre_step);
            DEF_SNAME(on_box2d_post_step);
            f(vm, self.world.GetBodyList(), on_box2d_pre_step);
            self.world.Step(dt, velocity_iterations, position_iterations);
            f(vm, self.world.GetBodyList(), on_box2d_post_step);

            // destroy bodies which are marked as destroyed
            b2Body* p = self.world.GetBodyList();
            while(p != nullptr){
                b2Body* next = p->GetNext();
                PyBody& body = _CAST(PyBody&, get_body_object(p));
                if(body._is_destroyed){
                    body.body->GetWorld()->DestroyBody(body.body);
                    body.body = nullptr;
                    body._fixture = nullptr;
                    body.node_like = nullptr;
                }
                p = next;
            }
            return vm->None;
        });

    vm->bind(type, "debug_draw(self, flags: int)", [](VM* vm, ArgsView args){
        PyWorld& self = _CAST(PyWorld&, args[0]);
        int flags = CAST(int, args[1]);
        self._debug_draw.SetFlags(flags);
        self.world.DebugDraw();
        return vm->None;
    });

    vm->bind(type, "set_debug_draw(self, draw: _DrawLike)", [](VM* vm, ArgsView args){
        PyWorld& self = _CAST(PyWorld&, args[0]);
        self._debug_draw.draw_like = args[1];
        return vm->None;
    });

    // joints
    vm->bind(type, "create_weld_joint(self, a, b)", [](VM* vm, ArgsView args){
        PyWorld& self = _CAST(PyWorld&, args[0]);
        PyBody& bodyA = CAST(PyBody&, args[1]);
        PyBody& bodyB = CAST(PyBody&, args[2]);
        b2WeldJointDef def;
        def.Initialize(bodyA.body, bodyB.body, bodyA.body->GetWorldCenter());
        b2Joint* p = self.world.CreateJoint(&def);
        return VAR(p);      // void_p
    });
}

}   // namespace pkpy

