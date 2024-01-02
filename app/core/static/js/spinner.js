
export const createSpinner = (containerId) => {
    var opts = {
        lines: 8,
        length: 28,
        width: 22,
        radius: 45,
        scale: 0.2,
        corners: 1,
        speed: 1.0,
        rotate: 0,
        animation: 'spinner-line-fade-default',
        direction: 1,
        color: '#000000',
        fadeColor: 'transparent',
        top: '51%',
        left: '50%',
        shadow: '0 0 1px transparent',
        zIndex: 2000000000,
        className: 'spinner',
        position: 'absolute',
    };

    var spinner = new Spinner(opts);
    var container = document.getElementById(containerId);
    spinner.spin(container);

    return spinner;
}