type Room = {
    id: number;
    width: number;
    height: number;
    anchorTopLeftX: number,
    anchorTopLeftY: number,
    type: "workRoom" | "meetRoom";
}

type Coords = {
    x: number;
    y: number;
}

type PlanBoundary = Coords[];

type Data = {
    planBoundary: PlanBoundary;
    rooms: Room[];
}

const defaultItem = {
    item_type: 8,
    rotation: 0,
    scale_x: 1,
    scale_y: 1,
    scale_z: 507,
    fixed: false
}

type Item = {
    item_name: "Arbeidsrom" | "Moterom";
    item_type?: number;
    model_url?: "models/js/work_room.js" | "models/js/meeting_room.js";
    xpos: number;
    ypos: number;
    zpos: number;
    rotation: number;
    scale_x: number;
    scale_y: number;
    scale_z: number;
    fixed: boolean;
}

type Corner = {
    [key: string]: Coords[]
}

type Wall = {
    corner1: string;
    corner2: string;
}

type Floorplan = {
    corners: Corner[];
    walls: any[];
}






const data: Data = {
    planBoundary: [
        {
            x: 0,
            y: 0
        },
        {
            x: 100,
            y: 0
        },
        {
            x: 100,
            y: 100
        },
        {
            x: 0,
            y: 100
        }
    ],
    rooms: [
        {
            id: 1,
            width: 20,
            height: 20,
            anchorTopLeftX: -100,
            anchorTopLeftY: 0,
            type: "workRoom"
        },
        {
            id: 2,
            width: 20,
            height: 20,
            anchorTopLeftX: -80,
            anchorTopLeftY: 0,
            type: "workRoom"
        },
        {
            id: 3,
            width: 20,
            height: 20,
            anchorTopLeftX: -80,
            anchorTopLeftY: 0,
            type: "workRoom"
        },
        {
            id: 4,
            width: 60,
            height: 20,
            anchorTopLeftX: -100,
            anchorTopLeftY: 20,
            type: "meetRoom"
        },
        {
            id: 4,
            width: 40,
            height: 20,
            anchorTopLeftX: -40,
            anchorTopLeftY: 20,
            type: "meetRoom"
        },
        {
            id: 4,
            width: 40,
            height: 40,
            anchorTopLeftX: -60,
            anchorTopLeftY: 40,
            type: "meetRoom"
        },
        {
            id: 4,
            width: 40,
            height: 40,
            anchorTopLeftX: -100,
            anchorTopLeftY: 40,
            type: "meetRoom"
        }
    ]
};


// WIP
/*export const transformData = (data: Data) => {
    const floorplan = {
        corners: [],
        walls: []
    };

    const items = [];
    
    for (const element of data.rooms){
        //check if work room or meeting room
        if (element.type === 'meetRoom'){
            items.push(
                {
                    ...defaultItem,

                }
            );


        } else if (element.type === 'workRoom'){
            items.push({
                ...defaultItem,
                item_name: 'Arbeidsrom',
                model_url: 'models/js/work_room.js',
                xpos: 
            })

        }


    }


};*/


